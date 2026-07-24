import { Button } from "@/components/ui/button";
import { contentTypeOptions } from "@/constants/contentTypes";
import { platforms } from "@/constants/platforms";
import { ScheduledPost } from "@/types/content";
import { Pencil, Trash2 } from "lucide-react";

interface Props {
  posts: ScheduledPost[];
  emptyLabel: string;
  onEdit?: (post: ScheduledPost) => void;
  onDelete?: (id: string) => void;
}

const statusStyles: Record<ScheduledPost["status"], { label: string; border: string; text: string }> = {
  draft: { label: "Draft", border: "border-l-slate-300", text: "text-slate-500" },
  scheduled: { label: "Scheduled", border: "border-l-blue-400", text: "text-blue-600" },
  queued: { label: "Queued", border: "border-l-amber-400", text: "text-amber-600" },
  published: { label: "Published", border: "border-l-emerald-400", text: "text-emerald-600" },
};

export default function PostList({ posts, emptyLabel, onEdit, onDelete }: Props) {
  if (posts.length === 0) {
    return (
      <div className="rounded-xl border border-dashed border-slate-200 bg-white p-10 text-center text-sm text-slate-400">
        {emptyLabel}
      </div>
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {posts.map((post) => {
        const typeOption = contentTypeOptions.find((c) => c.value === post.contentType);
        const Icon = typeOption?.icon;
        const status = statusStyles[post.status];

        return (
          <div
            key={post.id}
            className={`rounded-xl border border-l-4 border-slate-200 bg-white px-5 py-4 shadow-sm ${status.border}`}
          >
            <div className="flex items-center gap-4">
              <div className="min-w-0 flex-1">
                <div className="flex items-center gap-2">
                  {Icon && <Icon size={14} className="shrink-0 text-slate-400" />}
                  <p className="truncate text-sm font-semibold text-slate-800">
                    {post.scheduledTime} · {post.scheduledDate}
                  </p>
                </div>
                <p className="mt-1 truncate text-sm text-slate-600">{post.caption || "Untitled post"}</p>
              </div>

              <Button variant="outline" size="sm" className={`rounded-full pointer-events-none ${status.text}`}>
                {status.label}
              </Button>

              <div className="flex gap-1.5">
                {onEdit && (
                  <Button variant="outline" size="icon" className="h-8 w-8 rounded-full" onClick={() => onEdit(post)}>
                    <Pencil size={13} />
                  </Button>
                )}
                {onDelete && (
                  <Button
                    variant="outline"
                    size="icon"
                    className="h-8 w-8 rounded-full border-red-200 text-red-500 hover:bg-red-50"
                    onClick={() => onDelete(post.id)}
                  >
                    <Trash2 size={13} />
                  </Button>
                )}
              </div>
            </div>

            {post.platforms.length > 0 && (
              <div className="mt-3 flex items-center gap-1.5 border-t border-slate-100 pt-3">
                <span className="text-[11px] text-slate-400">Posting to</span>
                <div className="flex -space-x-1">
                  {post.platforms.map((name) => {
                    const p = platforms.find((pl) => pl.name === name);
                    if (!p) return null;
                    return (
                      <span
                        key={name}
                        className="flex h-5 w-5 items-center justify-center rounded-full text-white ring-1 ring-white"
                        style={p.brandColor.startsWith("linear-gradient") ? { backgroundImage: p.brandColor } : { backgroundColor: p.brandColor }}
                      >
                        <p.icon size={9} />
                      </span>
                    );
                  })}
                </div>
                {post.recurring !== "none" && (
                  <span className="ml-2 rounded-full bg-slate-100 px-2 py-0.5 text-[10px] font-medium capitalize text-slate-500">
                    Repeats {post.recurring}
                  </span>
                )}
              </div>
            )}
          </div>
        );
      })}
    </div>
  );
}