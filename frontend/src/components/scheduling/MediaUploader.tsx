"use client";

import { useRef, useState } from "react";
import { UploadCloud, X, Film } from "lucide-react";
import { ContentType } from "@/types/content";

interface Props {
  contentType: ContentType;
  files: File[];
  onChange: (files: File[]) => void;
}

const acceptMap: Record<ContentType, string> = {
  text: "",
  image: "image/*",
  video: "video/*",
  carousel: "image/*,video/*",
  story: "image/*,video/*",
  reel: "video/*",
};

const multipleAllowed: ContentType[] = ["carousel"];

export default function MediaUploader({ contentType, files, onChange }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [isDragging, setIsDragging] = useState(false);

  const isMultiple = multipleAllowed.includes(contentType);

  const addFiles = (incoming: FileList | null) => {
    if (!incoming || incoming.length === 0) return;
    const newFiles = Array.from(incoming);
    onChange(isMultiple ? [...files, ...newFiles] : [newFiles[0]]);
  };

  const removeFile = (index: number) => {
    onChange(files.filter((_, i) => i !== index));
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault();
    setIsDragging(false);
    addFiles(e.dataTransfer.files);
  };

  return (
    <div>
      <label className="text-sm font-semibold text-slate-600">
        {contentType === "carousel" ? "Media (add multiple)" : "Media"}
      </label>

      <div
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => {
          e.preventDefault();
          setIsDragging(true);
        }}
        onDragLeave={() => setIsDragging(false)}
        onDrop={handleDrop}
        className={`mt-3 flex cursor-pointer flex-col items-center justify-center gap-2 rounded-xl border-2 border-dashed px-6 py-10 text-center transition-colors duration-150 ${
          isDragging ? "border-slate-400 bg-slate-50" : "border-slate-200 hover:bg-slate-50"
        }`}
      >
        <UploadCloud size={24} className="text-slate-400" />
        <p className="text-sm font-medium text-slate-600">
          Click to upload or drag and drop
        </p>
        <p className="text-xs text-slate-400">
          {contentType === "video" || contentType === "reel" ? "MP4, MOV up to 100MB" : "PNG, JPG, MP4 up to 25MB"}
        </p>
        <input
          ref={inputRef}
          type="file"
          accept={acceptMap[contentType]}
          multiple={isMultiple}
          onChange={(e) => addFiles(e.target.files)}
          className="hidden"
        />
      </div>

      {files.length > 0 && (
        <div className="mt-4 grid grid-cols-3 gap-3 sm:grid-cols-4">
          {files.map((file, index) => {
            const url = URL.createObjectURL(file);
            const isVideo = file.type.startsWith("video");
            return (
              <div key={index} className="group relative aspect-square overflow-hidden rounded-lg border border-slate-200 bg-slate-100">
                {isVideo ? (
                  <div className="flex h-full w-full items-center justify-center">
                    <Film size={20} className="text-slate-400" />
                  </div>
                ) : (
                  // eslint-disable-next-line @next/next/no-img-element
                  <img src={url} alt={file.name} className="h-full w-full object-cover" />
                )}
                <button
                  type="button"
                  onClick={(e) => {
                    e.stopPropagation();
                    removeFile(index);
                  }}
                  className="absolute right-1.5 top-1.5 flex h-6 w-6 items-center justify-center rounded-full bg-black/60 text-white opacity-0 transition-opacity group-hover:opacity-100"
                >
                  <X size={13} />
                </button>
              </div>
            );
          })}
        </div>
      )}
    </div>
  );
}