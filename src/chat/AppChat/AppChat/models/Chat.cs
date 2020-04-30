using System;
using System.ComponentModel.DataAnnotations.Schema;
using System.Text.Json.Serialization;

namespace AppChat.models
{
    public class UserData
    {
        [JsonPropertyName("id")] public string Id { get; set; }
        [JsonPropertyName("username")] public string UserName { get; set; }
        [JsonPropertyName("image")] public string Image { get; set; }
        [JsonPropertyName("device_id")] public string DeviceId { get; set; }
    }

    public class Chat
    {
        [JsonPropertyName("id")] public Guid Id { get; set; }
        [JsonPropertyName("chat_creator")] public string ChatCreator { get; set; }
        [JsonPropertyName("requested_user")] public string RequestedUser { get; set; }
        [JsonPropertyName("status")] public string Status { get; set; } // 0 = Pending, 1 = Accepted, 2 = Rejected
        [JsonPropertyName("is_blocked")] public bool IsBlocked { get; set; }
        [JsonPropertyName("creation_date")] public DateTime? CreationDate { get; set; }

        [JsonPropertyName("last_modification")]
        public DateTime? LastModification { get; set; }

        [JsonPropertyName("creator_data")]
        [NotMapped]
        public UserData CreatorData { get; set; }

        [JsonPropertyName("requested_user_data")]
        [NotMapped]
        public UserData RequestedUserData { get; set; }
    }
}