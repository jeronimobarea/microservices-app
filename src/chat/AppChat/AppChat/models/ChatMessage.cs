using System;

namespace AppChat.models
{
    public class ChatMessage
    {
        public Guid Id { get; set; }
        public string ChatId { get; set; }
        public string CreatorId { get; set; }
        public string CreatorName { get; set; }
        public string Content { get; set; }
        public DateTime? CreationDate { get; set; }
    }
}