import { pipelineId } from "../services/util";
import { useNodeInteraction } from "@adalace/react";
import { useRouter } from "next/router";
import Link from "next/link";
import EvaluateImage from "./ActionComponents/EvaluateImage";
import EvaluateTranscription from "./ActionComponents/EvaluateTranscription";
import { Loader2 } from "lucide-react";

export default function ActionComponent() {
  const router = useRouter();
  const { taskId, actionId, isolateAction } = router.query;
  const { data, loading: actionLoading } = useNodeInteraction(
    pipelineId,
    Number(taskId),
    Number(actionId)
  );

  if (isolateAction) {
    return actionLoading ? (
      <div className="flex items-center justify-center h-screen">
        <div className="flex items-center justify-center h-8 w-8 rounded-full bg-muted dark:bg-muted-dark">
          <Loader2 className="h-4 w-4 animate-spin text-muted-foreground dark:text-muted-foreground-dark" />
        </div>
      </div>
    ) : (
      <div className="rounded-lg p-6 h-screen">
        {data &&
          (data.node_config.type == "evaluate_transcription" ? (
            <EvaluateTranscription />
          ) : data.node_config.type == "evaluate_image" ? (
            <EvaluateImage />
          ) : null)}
      </div>
    );
  } else {
    return (
      <div className="max-w-4xl mx-auto p-6">
        <Link
          href={`/tasks/${taskId}`}
          className="inline-block mb-6 text-blue-600 hover:text-blue-800 font-medium"
        >
          ← Back to Task
        </Link>

        {actionLoading ? (
          <div className="text-gray-500 animate-pulse">Loading...</div>
        ) : (
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4">Action {actionId}</h2>
            {data &&
              (data.node_config.type == "evaluate_transcription" ? (
                <EvaluateTranscription />
              ) : data.node_config.type == "evaluate_image" ? (
                <EvaluateImage />
              ) : null)}
          </div>
        )}
      </div>
    );
  }
}
