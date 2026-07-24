import { platforms } from "@/constants/platforms";
import { ContentType } from "@/types/content";
import { contentTypeOptions } from "@/constants/contentTypes";
import { useCurrentUser } from "@/hooks/useCurrentUser";
import { Film } from "lucide-react";

interface Props {
  caption: string;
  contentType: ContentType;
  selectedPlatforms: string[];
  mediaFiles: File[];
}

export default function ContentPreview({ caption, contentType, selectedPlatforms, mediaFiles }: Props) {
  const { name } = useCurrentUser();
  const initial = name.charAt(0).toUpperCase();
  const typeLabel = contentTypeOptions.find((c) => c.value === contentType)?.label ?? "Post";
  const previewPlatform = platforms.find((p) => selectedPlatforms.includes(p.name));

  return (
    <div className="overflow-hidden rounded-3xl border border-slate-200 bg-white shadow-lg transition-all duration-300 hover:shadow-xl">
      {/* Header */}
      <div className="flex items-center justify-between border-b border-slate-200 bg-slate-50 px-6 py-5">
        <h3 className="text-lg font-bold text-slate-900">
          Live Preview
        </h3>

      <span className="rounded-full bg-cyan-50 px-3 py-1 text-xs font-semibold text-cyan-700">
          {typeLabel}
      </span>
    </div>

      {/* Preview Body */}
      <div className="space-y-4 p-6">

        
        

        {/* Media */}
        {contentType !== "text" && (
          <div>
            {mediaFiles.length === 0 ? (
              <div className="flex aspect-video flex-col items-center justify-center rounded-2xl border border-dashed border-slate-300 bg-slate-50 text-slate-400">
                <Film size={32} className="mb-3" />

                <p className="text-sm font-medium">
                  {typeLabel} Preview
                </p>

                <p className="mt-1 text-xs">
                  Uploaded media will appear here
                </p>
              </div>
            ) : mediaFiles.length === 1 ? (
              <MediaThumb
                file={mediaFiles[0]}
                className="aspect-video w-full rounded-2xl"
              />
            ) : (
              <div className="flex gap-2 overflow-x-auto pb-1">
                {mediaFiles.map((file, i) => (
                  <MediaThumb
                    key={i}
                    file={file}
                    className="aspect-square w-24 shrink-0 rounded-xl"
                  />
                ))}
              </div>
            )}
          </div>
        )}

        {/* Caption */}
        <div className="rounded-2xl bg-slate-50 p-4">
          <p className="whitespace-pre-wrap text-[15px] leading-7 text-slate-700">
            {caption || "Your caption will appear here..."}
          </p>
        </div>

        {/* Footer */}
        {previewPlatform && (
          <div className="flex items-center gap-2 border-t border-slate-100 pt-5 text-sm text-slate-500">
            <span>Posting to</span>

            <span
              className="flex h-6 w-6 items-center justify-center rounded-full text-white shadow-sm"
              style={
                previewPlatform.brandColor.startsWith("linear-gradient")
                  ? { backgroundImage: previewPlatform.brandColor }
                  : { backgroundColor: previewPlatform.brandColor }
              }
            >
              <previewPlatform.icon size={11} />
            </span>

            <span className="font-medium text-slate-700">
              {selectedPlatforms.length > 1
                ? `${previewPlatform.name} +${selectedPlatforms.length - 1} more`
                : previewPlatform.name}
            </span>
          </div>
        )}
      </div>
    </div>
  );
}

function MediaThumb({
  file,
  className,
}: {
  file: File;
  className: string;
}) {
  const url = URL.createObjectURL(file);
  const isVideo = file.type.startsWith("video");

  if (isVideo) {
    return (
      <div
        className={`flex items-center justify-center overflow-hidden rounded-2xl border border-slate-200 bg-slate-100 ${className}`}
      >
        <Film size={28} className="text-slate-400" />
      </div>
    );
  }

  // eslint-disable-next-line @next/next/no-img-element
  return (
    <img
      src={url}
      alt={file.name}
      className={`object-cover ${className}`}
    />
  );
}