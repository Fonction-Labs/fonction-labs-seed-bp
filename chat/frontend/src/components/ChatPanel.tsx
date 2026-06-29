import { ChatKit, useChatKit } from "@openai/chatkit-react";
import { STARTER_PROMPTS } from "../lib/config";
import { getToken } from "../lib/auth";

const BACKEND_URL = import.meta.env.VITE_BACKEND_URL || "";
const CHATKIT_URL = BACKEND_URL ? `${BACKEND_URL}/chatkit` : "/chatkit";

function ChatPanelInner() {
  const token = getToken();
  const authFetch: typeof fetch = (input, init) => {
    const headers = new Headers(init?.headers);
    if (token) headers.set("Authorization", `Bearer ${token}`);
    return fetch(input, { ...init, headers });
  };
  const chatkit = useChatKit({
    api: {
      url: CHATKIT_URL,
      domainKey: "domain_pk_localhost_dev",
      fetch: authFetch,
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
