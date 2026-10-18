"use client";

import { MinimalAgent } from "@/lib/agents/types";
import { buildAgentAvatarUrl } from "@/lib/agents/utils";
import { SvgOnyxLogo } from "@opal/logos";
import { useSettings } from "@/lib/settings/hooks";
import { DEFAULT_AVATAR_SIZE_PX, DEFAULT_AGENT_ID } from "@/lib/constants";
import CustomAgentAvatar from "@/refresh-components/avatars/CustomAgentAvatar";
import Image from "next/image";
import { useTranslations } from "next-intl";

export interface AgentAvatarProps {
  agent: MinimalAgent;
  size?: number;
}

export default function AgentAvatar({
  agent,
  size = DEFAULT_AVATAR_SIZE_PX,
  ...props
}: AgentAvatarProps) {
  const t = useTranslations("common.agentAvatar");
  const { enterprise: enterpriseSettings } = useSettings();

  if (agent.id === DEFAULT_AGENT_ID) {
    const logoSrc = enterpriseSettings?.use_custom_logo
      ? "/api/enterprise-settings/logo"
      : "/prajna-logo.png";
    return (
      <div
        className="aspect-square rounded-full overflow-hidden relative shrink-0"
        style={{ height: size, width: size }}
      >
        <Image
          alt={t("logo.alt") || "Prajna Logo"}
          src={logoSrc}
          fill
          className="object-cover object-center"
          sizes={`${size}px`}
        />
      </div>
    );
  }

  return (
    <CustomAgentAvatar
      name={agent.name}
      src={agent.uploaded_image_id ? buildAgentAvatarUrl(agent.id) : undefined}
      iconName={agent.icon_name}
      size={size}
      {...props}
    />
  );
}
