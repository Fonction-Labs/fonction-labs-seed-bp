import { ChatPanel } from "./components/ChatPanel";
import { DashboardPanel } from "./components/DashboardPanel";

export default function App() {
  return (
    <div className="flex h-screen w-screen">
      <DashboardPanel />
      <ChatPanel />
    </div>
  );
}
