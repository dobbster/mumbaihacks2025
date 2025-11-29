import React, { useState } from "react";
import { Rss } from "lucide-react";

import {
  AssistantRuntimeProvider,
  ThreadPrimitive,
  ComposerPrimitive,
} from "@assistant-ui/react";
import { useChatRuntime, AssistantChatTransport } from "@assistant-ui/react-ai-sdk";

export default function NewsAssistant() {
  const [input, setInput] = useState("");

  // Create runtime for Assistant-UI
  const runtime = useChatRuntime({
    transport: {
      type: "web",
      url: "/api/chat",
    }
  });

  // Optional: your custom verify API
  const handleVerify = () => {
    runtime.sendMessage(input); // send message into assistant-ui
    setInput("");
  };

  return (
    <AssistantRuntimeProvider runtime={runtime}>
      <div className="max-w-3xl mx-auto p-6 bg-gray-900 text-white rounded-xl shadow-lg">
        
        {/* Header */}
        <div className="flex items-center gap-2 mb-6">
          <Rss className="w-6 h-6 text-orange-400" />
          <h2 className="text-2xl font-bold">News Verification Assistant</h2>
        </div>

        {/* Thread */}
        <ThreadPrimitive.Root className="aui-root aui-thread-root">
          <ThreadPrimitive.Viewport className="aui-thread-viewport h-64 overflow-y-auto">
            <ThreadPrimitive.Messages />
          </ThreadPrimitive.Viewport>

          {/* Composer */}
          <ComposerPrimitive.Root className="flex gap-2 mt-4">
            <ComposerPrimitive.Textarea
              placeholder="Enter news headline or URL..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              className="flex-1 bg-gray-800 p-3 rounded-lg text-white border border-gray-700 focus:outline-none"
            />

            <button
              onClick={handleVerify}
              className="px-5 py-2 bg-green-600 rounded-lg hover:bg-green-700 transition"
            >
              Verify
            </button>
          </ComposerPrimitive.Root>
        </ThreadPrimitive.Root>
      </div>
    </AssistantRuntimeProvider>
  );
}
