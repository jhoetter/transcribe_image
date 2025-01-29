import { useNodeInteraction } from "@adalace/react";
import { pipelineId } from "../../services/util";
import { useRouter } from "next/router";

interface TranscriptionData {
  interaction_data: {
    transcriptions: string[];
    image_urls: string[];
  };
}

export default function EvaluateTranscription() {
  const router = useRouter();
  const { taskId, actionId } = router.query;

  const {
    data,
    loading: actionLoading,
    submitInteraction,
    submitting,
  } = useNodeInteraction(pipelineId, Number(taskId), Number(actionId));

  const transcriptionData = data as unknown as TranscriptionData;

  console.log(transcriptionData);

  if (actionLoading) {
    return <div>Loading...</div>;
  }

  if (
    !transcriptionData?.interaction_data?.transcriptions ||
    !transcriptionData?.interaction_data?.image_urls
  ) {
    return <div>Missing transcriptions or images</div>;
  }

  const { transcriptions, image_urls } = transcriptionData.interaction_data;

  const handleConfirmation = async (areOk: boolean) => {
    try {
      await submitInteraction({ are_ok: areOk });
      console.log("Confirmation successful");
    } catch (error) {
      console.error("Confirmation failed:", error);
    }
  };

  return (
    <div className="space-y-4 max-w-3xl mx-auto">
      {transcriptions.map((transcription, index) => (
        <div key={index} className="p-4 rounded-lg">
          <div className="mb-4">
            <p className="text-gray-700 dark:text-gray-300">{transcription}</p>
          </div>
          <div>
            <img
              src={image_urls[index]}
              alt={`Generated image ${index + 1}`}
              className="max-w-full h-auto rounded-lg shadow-lg"
            />
          </div>
        </div>
      ))}

      <div className="flex justify-center gap-4 mt-6">
        <button
          onClick={() => handleConfirmation(true)}
          className="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
          disabled={submitting}
        >
          {submitting ? "Processing..." : "Approve"}
        </button>
        <button
          onClick={() => handleConfirmation(false)}
          className="px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600"
          disabled={submitting}
        >
          {submitting ? "Processing..." : "Reject"}
        </button>
      </div>
    </div>
  );
}
