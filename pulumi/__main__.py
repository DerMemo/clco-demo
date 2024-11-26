import pulumi
from pulumi_azure_native import resources, storage, web
from pulumi import FileArchive

# Resource Group
resource_group = resources.ResourceGroup("app-rg")

# Storage Account
account = storage.StorageAccount(
    "appstorage",
    resource_group_name=resource_group.name,
    sku=storage.SkuArgs(name="Standard_LRS"),
    kind="StorageV2"
)

# Storage Container
app_container = storage.BlobContainer(
    "app-container",
    account_name=account.name,
    resource_group_name=resource_group.name,
)

# Upload ZIP to Storage
blob = storage.Blob(
    "app-blob",
    resource_group_name=resource_group.name,
    account_name=account.name,
    container_name=app_container.name,
    type=storage.BlobType.BLOCK,
    source=FileArchive("./"),
)

# App Service Plan
app_service_plan = web.AppServicePlan(
    "app-service-plan",
    resource_group_name=resource_group.name,
    sku=web.SkuDescriptionArgs(
        tier="Free",
        name="F1"
    ),
    kind="Linux",
    reserved=True
)

# Web App
app = web.WebApp(
    "my-web-app",
    resource_group_name=resource_group.name,
    server_farm_id=app_service_plan.id,
    site_config=web.SiteConfigArgs(
        app_settings=[web.NameValuePairArgs(name="WEBSITE_RUN_FROM_PACKAGE", value="https://appstoragec260d52f.blob.core.windows.net/app-container/app-blob")],
        linux_fx_version="PYTHON|3.12",
    )
)

# Output the URL
pulumi.export("app_url", app.default_host_name)
