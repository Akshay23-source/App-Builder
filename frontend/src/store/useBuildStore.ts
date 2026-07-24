import { create } from "zustand";

export interface LogEntry {
  id: string;
  agent_role: string;
  event_type: string;
  message: string;
  timestamp: string;
  data?: any;
}

export interface TaskNodeData {
  id: string;
  task_key: string;
  name: string;
  agent_role: string;
  status: "PENDING" | "RUNNING" | "SUCCESS" | "FAILED";
  dependencies: string[];
}

export interface ProjectFile {
  path: string;
  content: string;
}

interface BuildStore {
  projectId: string | null;
  projectStatus: string;
  logs: LogEntry[];
  tasks: TaskNodeData[];
  files: ProjectFile[];
  activeAgent: string | null;
  previewUrl: string | null;

  setProject: (id: string, status: string, tasks?: TaskNodeData[], logs?: LogEntry[], files?: ProjectFile[]) => void;
  handleSocketEvent: (event: any) => void;
  addLog: (log: LogEntry) => void;
  setTasks: (tasks: TaskNodeData[]) => void;
}

export const useBuildStore = create<BuildStore>((set) => ({
  projectId: null,
  projectStatus: "QUEUED",
  logs: [],
  tasks: [
    { id: "planner", task_key: "planner", name: "Break idea into Task DAG", agent_role: "planner", status: "PENDING", dependencies: [] },
    { id: "research_design", task_key: "research_design", name: "Research Design & UX Patterns", agent_role: "research", status: "PENDING", dependencies: [] },
    { id: "generate_code", task_key: "generate_code", name: "Generate Application Code", agent_role: "codegen", status: "PENDING", dependencies: ["research_design"] },
    { id: "debug_build", task_key: "debug_build", name: "Sandbox Build & Typecheck", agent_role: "debug", status: "PENDING", dependencies: ["generate_code"] },
    { id: "generate_docs", task_key: "generate_docs", name: "Generate Project Documentation", agent_role: "docs", status: "PENDING", dependencies: ["debug_build"] },
  ],
  files: [],
  activeAgent: null,
  previewUrl: null,

  setProject: (id, status, tasks, logs, files) => set({
    projectId: id,
    projectStatus: status,
    tasks: tasks && tasks.length > 0 ? tasks : [
      { id: "planner", task_key: "planner", name: "Break idea into Task DAG", agent_role: "planner", status: "PENDING", dependencies: [] },
      { id: "research_design", task_key: "research_design", name: "Research Design & UX Patterns", agent_role: "research", status: "PENDING", dependencies: [] },
      { id: "generate_code", task_key: "generate_code", name: "Generate Application Code", agent_role: "codegen", status: "PENDING", dependencies: ["research_design"] },
      { id: "debug_build", task_key: "debug_build", name: "Sandbox Build & Typecheck", agent_role: "debug", status: "PENDING", dependencies: ["generate_code"] },
      { id: "generate_docs", task_key: "generate_docs", name: "Generate Project Documentation", agent_role: "docs", status: "PENDING", dependencies: ["debug_build"] },
    ],
    logs: logs || [],
    files: files || [],
  }),

  handleSocketEvent: (event) => set((state) => {
    const newLog: LogEntry = {
      id: Math.random().toString(),
      agent_role: event.agent_role,
      event_type: event.event_type,
      message: event.message,
      timestamp: event.timestamp || new Date().toISOString(),
      data: event.data,
    };

    let updatedTasks = [...state.tasks];
    if (event.task_id) {
      updatedTasks = updatedTasks.map((t) => {
        if (t.task_key === event.task_id || t.id === event.task_id) {
          const newStatus = event.event_type === "task_completed" ? "SUCCESS" : "RUNNING";
          return { ...t, status: newStatus };
        }
        return t;
      });
    }

    let updatedFiles = [...state.files];
    if (event.event_type === "file_created" && event.data?.path) {
      if (!updatedFiles.some((f) => f.path === event.data.path)) {
        updatedFiles.push({ path: event.data.path, content: "// Streamed file content..." });
      }
    }

    let newPreviewUrl = state.previewUrl;
    if (event.data?.preview_url) {
      newPreviewUrl = event.data.preview_url;
    }

    return {
      logs: [newLog, ...state.logs],
      tasks: updatedTasks,
      files: updatedFiles,
      activeAgent: event.agent_role,
      previewUrl: newPreviewUrl,
      projectStatus: event.event_type === "task_completed" && event.agent_role === "docs" ? "COMPLETED" : state.projectStatus,
    };
  }),

  addLog: (log) => set((state) => ({ logs: [log, ...state.logs] })),
  setTasks: (tasks) => set({ tasks }),
}));
