import os
from fastapi import APIRouter, Response, Cookie, Request
from fastapi.responses import FileResponse, JSONResponse
from typing import Any, Dict, List, Optional
from pydantic import BaseModel

router = APIRouter()

STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
LOGO_PATH = os.path.join(STATIC_DIR, "logo.png")

# ── Health & Version ──────────────────────────────────────────────────────────

@router.get("/health")
def health() -> Dict[str, str]:
    return {"status": "ok"}

@router.get("/version")
def version() -> Dict[str, str]:
    return {"backend_version": "v4.20.7"}

# ── Logo Endpoints ────────────────────────────────────────────────────────────

@router.api_route("/prajna-logo.png", methods=["GET", "HEAD"])
@router.api_route("/enterprise-settings/logo", methods=["GET", "HEAD"])
@router.api_route("/admin/enterprise-settings/logo", methods=["GET", "HEAD"])
def get_enterprise_logo():
    if os.path.exists(LOGO_PATH):
        return FileResponse(LOGO_PATH, media_type="image/png")
    return Response(status_code=404)

@router.api_route("/enterprise-settings/logotype", methods=["GET", "HEAD"])
@router.api_route("/admin/enterprise-settings/logotype", methods=["GET", "HEAD"])
def get_enterprise_logotype():
    if os.path.exists(LOGO_PATH):
        return FileResponse(LOGO_PATH, media_type="image/png")
    return Response(status_code=404)

# ── Auth & Users ──────────────────────────────────────────────────────────────

USERS_DB = {
    "admin": {
        "id": "person:admin",
        "email": "admin@prajna.ai",
        "display_name": "Admin",
        "role": "admin",
        "is_superuser": True
    },
    "harnish": {
        "id": "person:harnish",
        "email": "harnish@prajna.ai",
        "display_name": "Harnish Savsani",
        "role": "admin",
        "is_superuser": True
    },
    "rohan": {
        "id": "person:rohan",
        "email": "rohan@prajna.ai",
        "display_name": "Rohan Gaikwad",
        "role": "admin",
        "is_superuser": True
    },
    "ronit": {
        "id": "person:ronit",
        "email": "ronit@prajna.ai",
        "display_name": "Ronit Munde",
        "role": "admin",
        "is_superuser": True
    },
    "swati": {
        "id": "person:swati",
        "email": "swati@prajna.ai",
        "display_name": "Swati Gangurde",
        "role": "admin",
        "is_superuser": True
    }
}

@router.get("/auth/type")
def auth_type() -> Dict[str, str]:
    return {"auth_type": "disabled"}

@router.post("/auth/refresh")
def auth_refresh() -> Dict[str, str]:
    return {"access_token": "prajna-session-token", "token_type": "bearer"}

@router.get("/me")
def get_me(prajna_user: Optional[str] = Cookie(None)) -> Dict[str, Any]:
    current_key = prajna_user if prajna_user in USERS_DB else "admin"
    user_info = USERS_DB[current_key]

    return {
        "id": user_info["id"],
        "email": user_info["email"],
        "is_active": True,
        "is_superuser": user_info["is_superuser"],
        "is_verified": True,
        "role": user_info["role"],
        "account_type": "STANDARD",
        "team_name": "Engineering",
        "is_anonymous_user": False,
        "password_configured": False,
        "effective_permissions": ["admin", "basic"],
        "is_admin": True,
        "is_group_manager": False,
        "admin_capabilities": ["admin"],
        "preferences": {
            "chosen_assistants": [0],
            "visible_assistants": [0],
            "hidden_assistants": [],
            "pinned_assistants": [0],
            "default_model": "gpt-4o",
            "recent_assistants": [0],
            "auto_scroll": True,
            "shortcut_enabled": True,
            "temperature_override_enabled": True,
            "theme_preference": "system",
            "language": "en",
            "chat_background": None,
            "default_app_mode": "CHAT"
        },
        "personalization": {
            "name": user_info["display_name"],
            "role": "Founding Team",
            "memories": [],
            "use_memories": True,
            "enable_memory_tool": True,
            "user_preferences": ""
        }
    }

@router.get("/manage/users/accepted/all")
@router.get("/manage/users")
def get_all_users() -> List[Dict[str, Any]]:
    result = []
    for u in USERS_DB.values():
        result.append({
            "id": u["id"],
            "email": u["email"],
            "role": u["role"],
            "is_active": True,
            "is_superuser": u["is_superuser"],
            "is_verified": True,
            "account_type": "STANDARD"
        })
    return result

@router.put("/user/personalization")
@router.post("/user/personalization")
def update_personalization() -> Dict[str, Any]:
    return {"status": "ok"}

# ── Settings ──────────────────────────────────────────────────────────────────

@router.get("/settings")
def get_settings() -> Dict[str, Any]:
    return {
        "auto_scroll": True,
        "application_status": "active",
        "gpu_enabled": False,
        "maximum_chat_retention_days": 30,
        "notifications": [],
        "needs_reindexing": False,
        "anonymous_user_enabled": False,
        "invite_only_enabled": False,
        "deep_research_enabled": False,
        "multi_model_chat_enabled": True,
        "temperature_override_enabled": True,
        "reasoning_override_enabled": True,
        "model_routing_enabled": False,
        "hide_provider_grouping": False,
        "model_routing_model_configuration_id": None,
        "query_history_type": "normal",
        "hide_query_history_from_admin_panel": False,
        "search_ui_enabled": True,
        "user_knowledge_enabled": True,
        "show_extra_connectors": False,
        "hide_onyx_branding": True,
        "ee_features_enabled": True,
        "application_name": "Prajna"
    }

@router.get("/enterprise-settings")
def enterprise_settings() -> Dict[str, Any]:
    return {
        "application_name": "Prajna",
        "use_custom_logo": True,
        "use_custom_logotype": False,
        "logo_display_style": "logo_and_name",
        "custom_header_logo": "/api/enterprise-settings/logo",
        "custom_header_content": "Prajna Org Brain",
        "custom_lower_disclaimer_content": "[powered by FalkorDB](https://www.falkordb.com/)",
        "brand_color": "#12A885"
    }

@router.get("/enterprise-settings/custom-analytics-script")
def get_custom_analytics_script():
    return Response(content="", media_type="text/plain")

# ── License & Billing ─────────────────────────────────────────────────────────

@router.get("/license")
def get_license() -> Dict[str, Any]:
    return {
        "has_license": True,
        "seats": 100,
        "used_seats": 5,
        "plan_type": "annual",
        "issued_at": "2026-01-01T00:00:00Z",
        "expires_at": "2030-01-01T00:00:00Z",
        "grace_period_end": None,
        "status": "active",
        "expiry_warning_stage": "none",
        "source": "manual_upload",
        "trial_end": None
    }

@router.get("/admin/billing/billing-information")
@router.get("/tenants/billing-information")
def get_billing_information() -> Dict[str, Any]:
    return {
        "tenant_id": "kirana",
        "status": "active",
        "plan_type": "annual",
        "seats": 100,
        "billing_period": "annual",
        "current_period_start": "2026-01-01T00:00:00Z",
        "current_period_end": "2030-01-01T00:00:00Z",
        "cancel_at_period_end": False,
        "canceled_at": None,
        "trial_start": None,
        "trial_end": None
    }

# ── Notifications & Federated ─────────────────────────────────────────────────

@router.get("/notifications")
def get_notifications() -> List[Any]:
    return []

@router.get("/notifications/summary")
def get_notifications_summary() -> Dict[str, int]:
    return {"total_items": 0, "undismissed_count": 0}

@router.get("/federated")
def get_federated() -> List[Any]:
    return []

# ── Personas & Agents ─────────────────────────────────────────────────────────

@router.get("/persona")
@router.get("/persona/labels")
@router.get("/admin/persona")
@router.get("/admin/agents")
def get_personas() -> List[Dict[str, Any]]:
    return [
        {
            "id": 0,
            "name": "Prajna Org Brain",
            "description": "FalkorDB-powered Org Knowledge Teammate",
            "is_default": True,
            "is_visible": True,
            "tools": [],
            "document_sets": [],
            "llm_model_version_override": "gpt-4o",
            "starter_messages": [
                {"message": "Who knows the payments service?"},
                {"message": "What is the blast radius of auth?"},
                {"message": "Which features have the most complaints?"}
            ]
        }
    ]

@router.get("/persona/{agent_id}")
def get_persona(agent_id: int) -> Dict[str, Any]:
    return {
        "id": agent_id,
        "name": "Prajna Org Brain",
        "description": "FalkorDB-powered Org Knowledge Teammate",
        "is_default": True,
        "is_visible": True,
        "tools": [],
        "document_sets": [],
        "llm_model_version_override": "gpt-4o"
    }

@router.get("/admin/default-assistant/configuration")
def get_default_assistant_config() -> Dict[str, Any]:
    return {"default_assistant_id": 0}

# ── Language Models & Providers ───────────────────────────────────────────────

DEFAULT_PROVIDERS = [
    {
        "id": 1,
        "name": "OpenAI",
        "provider": "openai",
        "provider_display_name": "OpenAI",
        "api_key": None,
        "api_base": None,
        "api_version": None,
        "custom_config": None,
        "is_public": True,
        "is_auto_mode": False,
        "groups": [],
        "personas": [0],
        "deployment_name": None,
        "model_configurations": [
            {
                "id": 1,
                "name": "gpt-4o",
                "display_name": "GPT-4o",
                "is_visible": True,
                "max_input_tokens": 128000,
                "supports_image_input": True,
                "supports_reasoning": False,
                "is_recommended_default": True,
                "effectiveDisplayName": "GPT-4o"
            },
            {
                "id": 2,
                "name": "gpt-4o-mini",
                "display_name": "GPT-4o Mini",
                "is_visible": True,
                "max_input_tokens": 128000,
                "supports_image_input": True,
                "supports_reasoning": False,
                "is_recommended_default": False,
                "effectiveDisplayName": "GPT-4o Mini"
            }
        ],
        "next_model_configuration_offset": None
    },
    {
        "id": 2,
        "name": "OpenRouter",
        "provider": "openrouter",
        "provider_display_name": "OpenRouter",
        "api_key": None,
        "api_base": None,
        "api_version": None,
        "custom_config": None,
        "is_public": True,
        "is_auto_mode": False,
        "groups": [],
        "personas": [0],
        "deployment_name": None,
        "model_configurations": [
            {
                "id": 3,
                "name": "openai/gpt-4o",
                "display_name": "OpenRouter GPT-4o",
                "is_visible": True,
                "max_input_tokens": 128000,
                "supports_image_input": True,
                "supports_reasoning": False,
                "is_recommended_default": False,
                "effectiveDisplayName": "OpenRouter GPT-4o"
            }
        ],
        "next_model_configuration_offset": None
    },
    {
        "id": 3,
        "name": "LiteLLM Proxy",
        "provider": "litellm_proxy",
        "provider_display_name": "LiteLLM Proxy",
        "api_key": None,
        "api_base": "http://localhost:4000",
        "api_version": None,
        "custom_config": None,
        "is_public": True,
        "is_auto_mode": False,
        "groups": [],
        "personas": [0],
        "deployment_name": None,
        "model_configurations": [
            {
                "id": 4,
                "name": "gpt-4o",
                "display_name": "LiteLLM GPT-4o",
                "is_visible": True,
                "max_input_tokens": 128000,
                "supports_image_input": True,
                "supports_reasoning": False,
                "is_recommended_default": False,
                "effectiveDisplayName": "LiteLLM GPT-4o"
            }
        ],
        "next_model_configuration_offset": None
    }
]

LLM_STATE: Dict[str, Any] = {
    "providers": DEFAULT_PROVIDERS,
    "default_text": {"provider_id": 1, "model_name": "gpt-4o"},
    "default_vision": {"provider_id": 1, "model_name": "gpt-4o"},
    "default_chat_naming": {"provider_id": 1, "model_name": "gpt-4o-mini"},
    "default_craft": {"provider_id": 1, "model_name": "gpt-4o"}
}

@router.get("/llm/provider")
@router.get("/llm/persona/{agent_id}/providers")
@router.get("/admin/llm/provider")
def get_llm_providers() -> Dict[str, Any]:
    return LLM_STATE

@router.post("/admin/llm/default")
async def set_default_model(request: Request) -> Dict[str, Any]:
    body = await request.json()
    LLM_STATE["default_text"] = {
        "provider_id": body.get("provider_id", 1),
        "model_name": body.get("model_name", "gpt-4o")
    }
    return {"status": "ok"}

@router.post("/admin/llm/default-craft")
async def set_default_craft_model(request: Request) -> Dict[str, Any]:
    body = await request.json()
    LLM_STATE["default_craft"] = {
        "provider_id": body.get("provider_id", 1),
        "model_name": body.get("model_name", "gpt-4o")
    }
    return {"status": "ok"}

@router.delete("/admin/llm/default-craft")
def delete_default_craft_model() -> Dict[str, Any]:
    LLM_STATE["default_craft"] = None
    return {"status": "ok"}

@router.post("/admin/llm/test")
@router.post("/admin/llm/test/default")
def test_llm_provider() -> Dict[str, Any]:
    return {"status": "ok"}

@router.put("/admin/llm/provider")
async def put_llm_provider(request: Request) -> Dict[str, Any]:
    data = await request.json()
    provider_id = data.get("id")
    if not provider_id:
        provider_id = max([p["id"] for p in LLM_STATE["providers"]] + [0]) + 1
        data["id"] = provider_id
        LLM_STATE["providers"].append(data)
    else:
        for idx, p in enumerate(LLM_STATE["providers"]):
            if p["id"] == provider_id:
                LLM_STATE["providers"][idx] = data
                break
    return data

@router.delete("/admin/llm/provider/{provider_id}")
def delete_llm_provider(provider_id: int) -> Dict[str, Any]:
    LLM_STATE["providers"] = [p for p in LLM_STATE["providers"] if p["id"] != provider_id]
    return {"status": "ok"}

@router.get("/admin/llm/custom-provider-names")
def get_custom_provider_names() -> List[str]:
    return []

@router.post("/admin/llm/model-routing")
def update_model_routing() -> Dict[str, Any]:
    return {"status": "ok"}

@router.get("/admin/cost-overrides")
def get_cost_overrides() -> List[Any]:
    return []

@router.post("/admin/cost-overrides")
@router.put("/admin/cost-overrides")
@router.delete("/admin/cost-overrides")
def modify_cost_overrides() -> Dict[str, Any]:
    return {"status": "ok"}

@router.post("/admin/llm/openrouter/available-models")
def get_openrouter_models() -> Dict[str, Any]:
    return {
        "models": [
            {"id": 3, "name": "openai/gpt-4o", "display_name": "OpenRouter GPT-4o", "is_visible": True}
        ]
    }

@router.post("/admin/llm/litellm_proxy/available-models")
def get_litellm_models() -> Dict[str, Any]:
    return {
        "models": [
            {"id": 4, "name": "gpt-4o", "display_name": "LiteLLM GPT-4o", "is_visible": True}
        ]
    }

# ── Connectors & Credentials ──────────────────────────────────────────────────

@router.get("/manage/connector")
@router.get("/manage/admin/connector")
def get_connectors() -> List[Any]:
    return []

@router.post("/manage/connector")
@router.post("/manage/admin/connector")
def create_connector() -> Dict[str, Any]:
    return {"id": 1, "name": "connector"}

@router.get("/manage/connector/{id}")
@router.get("/manage/admin/connector/{id}")
def get_connector(id: int) -> Dict[str, Any]:
    return {"id": id, "name": "connector"}

@router.delete("/manage/connector/{id}")
@router.delete("/manage/admin/connector/{id}")
def delete_connector(id: int) -> Dict[str, Any]:
    return {"status": "ok"}

@router.get("/manage/admin/connector/indexing-status")
def get_indexing_status() -> List[Any]:
    return []

@router.get("/manage/admin/cc-pair")
def get_cc_pairs() -> List[Any]:
    return []

@router.get("/manage/admin/cc-pair/{id}")
def get_cc_pair(id: int) -> Dict[str, Any]:
    return {}

@router.get("/manage/document-set")
def get_document_sets() -> List[Any]:
    return []

@router.get("/manage/admin/credential")
def get_credentials() -> List[Any]:
    return []

@router.post("/manage/admin/credential")
def create_credential() -> Dict[str, Any]:
    return {"id": 1}

@router.delete("/manage/admin/credential/{id}")
def delete_credential(id: int) -> Dict[str, Any]:
    return {"status": "ok"}

@router.get("/manage/admin/similar-credentials/{source}")
def get_similar_credentials(source: str) -> List[Any]:
    return []

@router.get("/manage/admin/credential/capability-reports")
def get_credential_capability_reports() -> List[Any]:
    return []

@router.get("/connector/oauth/details/{source}")
def get_oauth_details(source: str) -> Dict[str, Any]:
    return {
        "oauth_enabled": False,
        "supports_manual_credentials": True,
        "additional_kwargs": []
    }

@router.get("/manage/admin/user-group")
def get_user_groups() -> List[Any]:
    return []

# ── Chat & Sessions ───────────────────────────────────────────────────────────

@router.post("/chat/create-chat-session")
def create_session() -> Dict[str, str]:
    return {"chat_session_id": "session-default-1"}

@router.get("/chat/get-user-chat-sessions")
def get_sessions() -> Dict[str, Any]:
    return {
        "sessions": [
            {
                "chat_session_id": "session-default-1",
                "description": "Org Graph Workspace",
                "persona_id": 0,
                "time_created": "2026-10-18T00:00:00Z"
            }
        ]
    }

@router.get("/chat/get-chat-session/{id}")
def get_chat_session(id: str) -> Dict[str, Any]:
    return {
        "chat_session_id": id,
        "description": "Org Graph Workspace",
        "persona_id": 0,
        "messages": []
    }

@router.get("/chat/incognito-availability")
def get_incognito_availability() -> Dict[str, bool]:
    return {"is_available": False}

@router.put("/chat/rename-chat-session")
def rename_chat_session() -> Dict[str, str]:
    return {"status": "ok"}

@router.put("/chat/update-chat-session-temperature")
def update_chat_session_temperature() -> Dict[str, str]:
    return {"status": "ok"}

@router.get("/manage/connector-status")
def get_connector_status() -> Dict[str, Any]:
    return {"connectors": [], "total": 0}
