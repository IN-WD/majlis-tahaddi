.class public Lcom/majlis/tahaddi/Bridge;
.super Ljava/lang/Object;

.field private final act:Landroid/app/Activity;

.method public constructor <init>(Landroid/app/Activity;)V
    .registers 2
    invoke-direct {p0}, Ljava/lang/Object;-><init>()V
    iput-object p1, p0, Lcom/majlis/tahaddi/Bridge;->act:Landroid/app/Activity;
    return-void
.end method

.method public setOrientation(I)V
    .registers 3
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lcom/majlis/tahaddi/Bridge;->act:Landroid/app/Activity;
    invoke-virtual {v0, p1}, Landroid/app/Activity;->setRequestedOrientation(I)V
    return-void
.end method

.method public cast()V
    .registers 4
    .annotation runtime Landroid/webkit/JavascriptInterface;
    .end annotation
    iget-object v0, p0, Lcom/majlis/tahaddi/Bridge;->act:Landroid/app/Activity;

    :try_start_0
    new-instance v1, Landroid/content/Intent;
    const-string v2, "android.settings.CAST_SETTINGS"
    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
    invoke-virtual {v0, v1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_0
    .catch Ljava/lang/Exception; {:try_start_0 .. :try_end_0} :catch_0
    return-void

    :catch_0
    :try_start_1
    new-instance v1, Landroid/content/Intent;
    const-string v2, "android.settings.DISPLAY_SETTINGS"
    invoke-direct {v1, v2}, Landroid/content/Intent;-><init>(Ljava/lang/String;)V
    invoke-virtual {v0, v1}, Landroid/app/Activity;->startActivity(Landroid/content/Intent;)V
    :try_end_1
    .catch Ljava/lang/Exception; {:try_start_1 .. :try_end_1} :catch_1

    :catch_1
    return-void
.end method
