"use client";
import { useSearchParams, useRouter } from "next/navigation";
import { ChatPage } from "../pages/ChatPage";
import { AuthGuard } from "../components/AuthGuard";

export default function Chat() {
  const searchParams = useSearchParams();
  const router = useRouter();
  const connectionId = searchParams.get("connectionId");

  if (!connectionId) {
    router.push("/");
    return null;
  }

  return (
    <AuthGuard>
      <ChatPage connectionId={connectionId} />
    </AuthGuard>
  );
}