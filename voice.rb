#require "google/cloud/speech"
require 'pocketsphinx-ruby' # Omitted in subsequent example

project_id = "kenekt"

# require "google/cloud/storage"

# If you don't specify credentials when constructing the client, the client
# library will look for credentials in the environment.
# storage = Google::Cloud::Storage.new project: project_id

# Make an authenticated API request
# storage.buckets.each do |bucket|
  # puts bucket.name
# end


microphone = Pocketsphinx::Microphone.new

File.open("test.raw", "wb") do |file|
  microphone.record do
    FFI::MemoryPointer.new(:int16, 2048) do |buffer|
      500.times do
        sample_count = microphone.read_audio(buffer, 2048)
        file.write buffer.get_bytes(0, sample_count * 2)

        sleep 0.1
      end
    end
  end
end


#
#
# speech = Google::Cloud::Speech.speech
#
# audio_file = File.binread audio_file_path
#
# config = { encoding:                 :LINEAR16,
#            sample_rate_hertz:        16_000,
#            language_code:            "en-US",
#            enable_word_time_offsets: true }
# audio  = { content: audio_file }
#
# response = speech.recognize config: config, audio: audio
#
# results = response.results
#
# alternatives = results.first.alternatives
# alternatives.each do |alternative|
#   puts "Transcription: #{alternative.transcript}"
#
#   alternative.words.each do |word|
#     start_time = word.start_time.seconds + (word.start_time.nanos / 1_000_000_000.0)
#     end_time   = word.end_time.seconds + (word.end_time.nanos / 1_000_000_000.0)
#
#     puts "Word: #{word.word} #{start_time} #{end_time}"
#   end
# end
