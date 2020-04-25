using System;
using System.Text.Json.Serialization;

namespace AppChat.models
{
    public class ChatMessage
    {
        [JsonPropertyName("id")] public Guid Id { get; set; }
        [JsonPropertyName("chat_id")] public string ChatId { get; set; }
        [JsonPropertyName("creator_id")] public string CreatorId { get; set; }
        [JsonPropertyName("content")] public string Content { get; set; }
        [JsonPropertyName("creation_date")] public DateTime? CreationDate { get; set; }
    }
}