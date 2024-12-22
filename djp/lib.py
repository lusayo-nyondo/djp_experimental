def setting_exists(
    setting: str,
    current_settings
):
    """
    Checking if particular settings are available in project settings.
    """
    if setting in [
        'INSTALLED_APPS',
        'MIDDLEWARE',
        'DATABASES',
        'STATICFILES_DIRS',
        'STATICFILES_FINDERS',
        'AUTH_PASSWORD_VALIDATORS',
        'AUTHENTICATION_BACKENDS',
        'ADMIN_SIDEBAR_ITEMS',
    ]:
        return setting in current_settings.keys()
    elif setting in [
        'CONTEXT_PROCESSORS',
        'LOADERS',
        'BUILTINS',
    ]:
        has_templates_setting = "TEMPLATES" in current_settings.keys()

        if not has_templates_setting:
            return False

        template_confs = current_settings["TEMPLATES"]
        
        if not isinstance(template_confs, list):
            raise Exception("TEMPLATES setting is not a list.")
        
        if len(template_confs) < 1:
            return False
        
        default_template = template_confs[0]
        
        if "OPTIONS" not in default_template.keys():
            return False
        
        template_options = default_template["OPTIONS"]
        
        if not isinstance(template_options, dict):
            raise Exception("OPTIONS setting within TEMPLATES is not a dict.")
        
        return setting.lower() in template_options.keys()
    else:
        raise Exception("Unsupported setting.")

