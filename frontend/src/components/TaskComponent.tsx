import { usePipelineTask } from "@adalace/react";
import { pipelineId } from "../services/util";
import { useRouter } from "next/router";
import Link from "next/link";

export default function TaskComponent() {
  const router = useRouter();
  const { taskId } = router.query;
  const { task, loading: taskLoading } = usePipelineTask(
    pipelineId,
    Number(taskId)
  );

  return (
    <div className="max-w-4xl mx-auto p-6">
      <Link
        href="/"
        className="inline-block mb-6 text-blue-600 hover:text-blue-800 font-medium"
      >
        ← Back to Tasks
      </Link>

      {taskLoading ? (
        <div className="text-gray-500 animate-pulse">Loading...</div>
      ) : (
        <div className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-2xl font-bold mb-4">Task {task?.id}</h2>
            <pre className="bg-gray-50 p-4 rounded-lg overflow-auto">
              {JSON.stringify(task?.input_data, null, 2)}
            </pre>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h3 className="text-xl font-semibold mb-4">Actions</h3>
            <ul className="space-y-4">
              {task?.actions.map((action) => (
                <li
                  key={action.id}
                  className="hover:bg-gray-50 p-4 rounded-lg transition-colors border border-gray-100"
                >
                  <div className="flex items-center justify-between mb-2">
                    <Link
                      href={`/tasks/${task.id}/actions/${action.id}`}
                      className="text-blue-600 hover:text-blue-800 font-medium"
                    >
                      Action {action.id}
                    </Link>
                    <span className="px-3 py-1 rounded-full text-sm">
                      {action.state}
                    </span>
                  </div>
                  <div className="text-sm text-gray-600">
                    <p>
                      <span className="font-medium">Node:</span>{" "}
                      {action.node_name}
                    </p>
                    <p>
                      <span className="font-medium">Created:</span>{" "}
                      {new Date(action.created_at).toLocaleString()}
                    </p>
                    {action.automated !== undefined && (
                      <p>
                        <span className="font-medium">Type:</span>{" "}
                        {action.automated ? "Automated" : "Manual"}
                      </p>
                    )}
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </div>
      )}
    </div>
  );
}
