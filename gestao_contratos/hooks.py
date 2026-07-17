app_name = "gestao_contratos"
app_title = "Gestao Contratos"
app_publisher = "StillPulse"
app_description = (
	"Gestão de projetos, contratos, expedientes e pessoas — "
	"funcionalidades do Axior no ERPNext (Desk nativo)."
)
app_email = "contato@stillpulse.com"
app_license = "mit"
app_version = "0.2.0"

required_apps = ["frappe", "erpnext"]

after_install = "gestao_contratos.setup.after_install"
after_migrate = "gestao_contratos.setup.after_migrate"

# fixtures = []

# scheduler_events = {}

# doc_events = {}

# override_doctype_class = {}

# doctype_js = {}
# doctype_list_js = {}

# app_include_css = "/assets/gestao_contratos/css/gestao_contratos.css"
# app_include_js = "/assets/gestao_contratos/js/gestao_contratos.js"
