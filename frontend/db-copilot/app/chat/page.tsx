"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { ChatPage } from "../pages/ChatPage";

export default function Chat() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const connectionId = searchParams.get("connectionId");

  if (!connectionId) {
    router.push("/");
    return null;
  }

  const handleDisconnect = () => {
    router.push("/");
  };

  return <ChatPage connectionId={connectionId} onDisconnect={handleDisconnect} />;
}