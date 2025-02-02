from aws_cdk import (
    Stack,
    aws_lambda as _lambda,
    aws_apigateway as apigw,
    aws_kinesis as kinesis,
    aws_dynamodb as dynamodb,
    aws_lambda_event_sources as event_sources,
    Duration
)
from constructs import Construct


class AnalyticsPipelineStack(Stack):
    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # Create Kinesis Data Stream
        stream = kinesis.Stream(self, "AnalyticsDataStream",
                                stream_mode=kinesis.StreamMode.ON_DEMAND
                                )

        # Create DynamoDB table
        table = dynamodb.Table(self, "AnalyticsTable",
                               partition_key=dynamodb.Attribute(
                                   name="id",
                                   type=dynamodb.AttributeType.STRING
                               ),
                               sort_key=dynamodb.Attribute(
                                   name="timestamp",
                                   type=dynamodb.AttributeType.STRING
                               ),
                               billing_mode=dynamodb.BillingMode.PAY_PER_REQUEST,
                               removal_policy=RemovalPolicy.DESTROY
                               )

        # Add GSI for category-based queries
        table.add_global_secondary_index(
            index_name="category-timestamp-index",
            partition_key=dynamodb.Attribute(
                name="category",
                type=dynamodb.AttributeType.STRING
            ),
            sort_key=dynamodb.Attribute(
                name="timestamp",
                type=dynamodb.AttributeType.STRING
            )
        )

        # Create Lambda functions
        ingestion_lambda = _lambda.Function(self, "DataIngestionFunction",
                                            runtime=_lambda.Runtime.PYTHON_3_9,
                                            handler="data_ingestion.handler",
                                            code=_lambda.Code.from_asset("app/lambda_functions"),
                                            environment={
                                                "KINESIS_STREAM_NAME": stream.stream_name
                                            },
                                            timeout=Duration.seconds(30)
                                            )

        processor_lambda = _lambda.Function(self, "DataProcessorFunction",
                                            runtime=_lambda.Runtime.PYTHON_3_9,
                                            handler="data_processor.handler",
                                            code=_lambda.Code.from_asset("app/lambda_functions"),
                                            environment={
                                                "DYNAMODB_TABLE_NAME": table.table_name
                                            },
                                            timeout=Duration.seconds(60)
                                            )

        analytics_lambda = _lambda.Function(self, "AnalyticsAPIFunction",
                                            runtime=_lambda.Runtime.PYTHON_3_9,
                                            handler="analytics_api.handler",
                                            code=_lambda.Code.from_asset("app/lambda_functions"),
                                            environment={
                                                "DYNAMODB_TABLE_NAME": table.table_name
                                            },
                                            timeout=Duration.seconds(30)
                                            )

        # Grant permissions
        stream.grant_write(ingestion_lambda)
        stream.grant_read(processor_lambda)
        table.grant_write_data(processor_lambda)
        table.grant_read_data(analytics_lambda)

        # Add Kinesis trigger to processor Lambda
        processor_lambda.add_event_source(
            event_sources.KinesisEventSource(stream,
                                             starting_position=_lambda.StartingPosition.LATEST,
                                             batch_size=100,
                                             max_batching_window=Duration.seconds(60)
                                             )
        )

        # Create API Gateway
        api = apigw.RestApi(self, "AnalyticsAPI")

        # Add API routes
        api.root.add_resource("ingest").add_method(
            "POST",
            apigw.LambdaIntegration(ingestion_lambda)
        )

        analytics = api.root.add_resource("analytics")
        analytics.add_method(
            "GET",
            apigw.LambdaIntegration(analytics_lambda)
        )