import * as React from "react";
import {
  usePipeline,
  usePipelineTasks,
  usePipelineExecution,
} from "@adalace/react";
import { pipelineId } from "../services/util";
import Link from "next/link";
import { useState } from "react";

export default function TasksOverview() {
  const { pipeline, loading: pipelineLoading } = usePipeline(pipelineId);
  const {
    tasks,
    loading: tasksLoading,
    fetchTasks,
  } = usePipelineTasks(pipelineId);
  const { executePipeline, executing } = usePipelineExecution(pipelineId);

  const [files, setFiles] = useState<File[]>([]);
  const [inputData, setInputData] = useState<string>("{}");
  const [showForm, setShowForm] = useState(false);

  const handleCreateTask = async () => {
    try {
      let parsedInput = {};
      try {
        parsedInput = JSON.parse(inputData);
      } catch (e) {
        console.error("Invalid JSON input:", e);
        return;
      }

      await executePipeline(parsedInput, files);
      setShowForm(false);
      setFiles([]);
      setInputData("{}");
      await fetchTasks();
    } catch (error) {
      console.error("Failed to create task:", error);
    }
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files) {
      setFiles(Array.from(e.target.files));
    }
  };

  return (
    <div className="max-w-4xl mx-auto p-6">
      {pipelineLoading ? (
        <p className="text-gray-500 animate-pulse">Loading...</p>
      ) : (
        <div className="mb-8">
          <div className="flex justify-between items-center mb-2">
            <h2 className="text-3xl font-bold">{pipeline?.name}</h2>
            <button
              onClick={() => setShowForm(!showForm)}
              className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg"
            >
              {showForm ? "Cancel" : "New Task"}
            </button>
          </div>
          <p className="text-gray-600">{pipeline?.description}</p>

          {showForm && (
            <div className="mt-4 p-4 bg-gray-50 rounded-lg">
              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Input Data (JSON)
                </label>
                <textarea
                  value={inputData}
                  onChange={(e) => setInputData(e.target.value)}
                  className="w-full h-32 p-2 border rounded-md font-mono text-sm"
                  placeholder="{}"
                />
              </div>

              <div className="mb-4">
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Files
                </label>
                <input
                  type="file"
                  multiple
                  onChange={handleFileChange}
                  className="block w-full text-sm text-gray-500
                    file:mr-4 file:py-2 file:px-4
                    file:rounded-full file:border-0
                    file:text-sm file:font-semibold
                    file:bg-blue-50 file:text-blue-700
                    hover:file:bg-blue-100"
                />
                {files.length > 0 && (
                  <div className="mt-2 text-sm text-gray-500">
                    Selected files: {files.map((f) => f.name).join(", ")}
                  </div>
                )}
              </div>

              <button
                onClick={handleCreateTask}
                disabled={executing}
                className="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg disabled:opacity-50"
              >
                {executing ? "Creating..." : "Create Task"}
              </button>
            </div>
          )}
        </div>
      )}
      {tasksLoading ? (
        <p className="text-gray-500 animate-pulse">Loading tasks...</p>
      ) : (
        <ul className="space-y-4">
          {tasks?.items?.map((task) => (
            <li
              key={task.id}
              className="border border-gray-200 hover:bg-gray-50 p-4 rounded-lg transition-colors"
            >
              <div className="flex justify-between items-start">
                <div>
                  <Link
                    href={`/tasks/${task.id}`}
                    className="text-blue-600 hover:text-blue-800 font-medium text-lg"
                  >
                    Task {task.id}
                  </Link>
                  <div className="mt-2 text-sm text-gray-600">
                    <p>
                      <span className="font-medium">Created:</span>{" "}
                      {new Date(task.created_at).toLocaleString()}
                    </p>
                    {task.uploaded_files && task.uploaded_files.length > 0 && (
                      <p>
                        <span className="font-medium">Files:</span>{" "}
                        {task.uploaded_files.join(", ")}
                      </p>
                    )}
                  </div>
                </div>
                <div className="text-sm">
                  <p className="mt-2">
                    <span className="font-medium">Actions:</span>{" "}
                    {task.actions.length}
                  </p>
                </div>
              </div>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}
