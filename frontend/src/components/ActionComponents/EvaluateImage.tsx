import { useNodeInteraction } from "@adalace/react";
import { pipelineId } from "../../services/util";
import { useRouter } from "next/router";

interface ImageData {
  interaction_data: {
    image_urls: string[];
  };
}

export default function EvaluateImage() {
  const router = useRouter();
  const { taskId, actionId } = router.query;

  const {
    data,
    loading: actionLoading,
    submitInteraction,
    submitting,
  } = useNodeInteraction(pipelineId, Number(taskId), Number(actionId));

  const imageData = data as unknown as ImageData;

  if (actionLoading) {
    return <div>Loading...</div>;
  }

  if (!imageData?.interaction_data?.image_urls) {
    return <div>Missing images</div>;
  }

  const { image_urls } = imageData.interaction_data;

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
      {image_urls.map((image_url, index) => (
        <div key={index} className="rounded-lg">
          <img
            src={image_url}
            alt={`Generated image ${index + 1}`}
            className="max-w-full h-auto rounded-lg shadow-lg"
          />
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
