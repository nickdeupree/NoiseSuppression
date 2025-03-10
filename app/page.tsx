"use client";

import { useState } from "react";
import { Link } from "@heroui/link";
import { Snippet } from "@heroui/snippet";
import { Code } from "@heroui/code";
import { button as buttonStyles } from "@heroui/theme";

import {Card, CardHeader, CardBody, CardFooter} from "@heroui/card";
import {Form} from "@heroui/form";
import { Input } from "@heroui/input";
import { Button } from "@heroui/button";
import { Progress } from "@heroui/progress";

import {processAudio} from "./api/audioService/route";

export default function Home() {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const[processedAudioUrl, setProcessedAudioUrl] = useState<string | null>(null);
  const [originalAudioUrl, setOriginalAudioUrl] = useState<string | null>(null);
  const [isProcessing, setIsProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);


  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if(e.target.files && e.target.files.length > 0) {
      const file = e.target.files[0];
      setSelectedFile(file);

      const url = URL.createObjectURL(file);
      setOriginalAudioUrl(url);

      setProcessedAudioUrl(null);
      setError(null);
    }
  };

  const handleProcessAudio = async () => {
    if (!selectedFile) {
      setError("Please select an audio file first");
      return;
    }

    try {
      setIsProcessing(true);
      setError(null);
      
      const processedAudioBlob = await processAudio(selectedFile);
      const url = URL.createObjectURL(processedAudioBlob);
      setProcessedAudioUrl(url);
    } catch (err) {
      setError(`Error processing audio: ${err instanceof Error ? err.message : String(err)}`);
    } finally {
      setIsProcessing(false);
    }
  };


  return (
    <section className="flex flex-col items-center justify-center gap-4 py-8 md:py-10">
      <Card
        isBlurred
        className="w-full max-w-lg"
      >
        <CardHeader className="flex justify-center">
          <p className="text-xl font-bold">Audio Noise Suppression</p>
        </CardHeader>
        <CardBody className="flex flex-col gap-4">
          <div>
            <Input
              classNames={{
                label: "text-black/50 dark:text-white/90",
                input: [
                  "bg-transparent",
                  "text-black/90 dark:text-white/90",
                  "placeholder:text-default-700/50 dark:placeholder:text-white/60",
                ],
                innerWrapper: "bg-transparent",
                inputWrapper: [
                  "shadow-xl",
                  "bg-default-200/50",
                  "dark:bg-default/60",
                  "backdrop-blur-xl",
                  "backdrop-saturate-200",
                  "hover:bg-default-200/70",
                  "dark:hover:bg-default/70",
                  "group-data-[focus=true]:bg-default-200/50",
                  "dark:group-data-[focus=true]:bg-default/60",
                  "!cursor-text",
                ],
              }}
              label="Upload Audio"
              placeholder="Select an audio file"
              radius="lg"
              type="file"
              accept="audio/*"
              onChange={handleFileChange}
            />
          </div>
          
          {error && (
            <div className="text-red-500 text-sm p-2 border border-red-300 rounded-md bg-red-50 dark:bg-red-900/20">
              {error}
            </div>
          )}
          
          {isProcessing && (
            <div className="flex flex-col gap-2">
              <p>Processing audio...</p>
              <Progress 
                size="sm"
                isIndeterminate
                aria-label="Processing audio..." 
                className="max-w-md" 
              />
            </div>
          )}
          
          <Button
            className={[
              "shadow-xl",
              "bg-default-200/50",
              "dark:bg-default/60",
              "backdrop-blur-xl",
              "backdrop-saturate-200",
              "hover:bg-default-200/70",
              "dark:hover:bg-default/70",
              "group-data-[focus=true]:bg-default-200/50",
              "dark:group-data-[focus=true]:bg-default/60",
            ].join(" ")}
            onClick={handleProcessAudio}
            isDisabled={!selectedFile || isProcessing}
          >
            <span className="flex items-center gap-2">
              Process Audio
            </span>
          </Button>
        </CardBody>
        
        {(originalAudioUrl || processedAudioUrl) && (
          <CardFooter className="flex flex-col gap-4">
            {originalAudioUrl && (
              <div className="w-full">
                <p className="text-sm mb-1 font-medium">Original Audio:</p>
                <audio controls className="w-full">
                  <source src={originalAudioUrl} type={selectedFile?.type} />
                  Your browser does not support the audio element.
                </audio>
              </div>
            )}
            
            {processedAudioUrl && (
              <div className="w-full">
                <p className="text-sm mb-1 font-medium">Processed Audio:</p>
                <audio controls className="w-full">
                  <source src={processedAudioUrl} />
                  Your browser does not support the audio element.
                </audio>
                <div className="mt-2">
                  <a 
                    href={processedAudioUrl} 
                    download={`processed_${selectedFile?.name}`}
                    className="text-sm text-blue-600 dark:text-blue-400 hover:underline"
                  >
                    Download processed audio
                  </a>
                </div>
              </div>
            )}
          </CardFooter>
        )}
      </Card>
    </section>
  );
}
