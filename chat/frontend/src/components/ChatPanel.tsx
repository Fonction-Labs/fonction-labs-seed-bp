import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { STARTER_PROMPTS } from "../lib/config";

function ChatPanelInner() {
  const chatkit = useChatKit({
    api: {
      url: "/chatkit",
      domainKey: "domain_pk_localhost_dev",
    },
    startScreen: {
      greeting: "Pose-moi des questions sur le BP : revenus, ARR, hypothèses, cash, headcount...",
      prompts: STARTER_PROMPTS,
    },
  });

  return <ChatKit {...chatkit} />;
}

export function ChatPanel() {
  return (
    <div className="w-[420px] h-full flex flex-col bg-white border-l border-gray-100 flex-shrink-0">
      <ChatPanelInner />
    </div>
  );
}
