using System;

namespace AppChat.models
{
    public class Chat
    {
        public Guid Id { get; set; }
        public string ChatCreator { get; set; }
        public string RequestedUser { get; set; }
        public string Status { get; set; } // 0 = Pending, 1 = Accepted, 2 = Rejected
        public bool IsBlocked { get; set; }
        public DateTime? CreationDate { get; set; }
        public DateTime? LastModification { get; set; }
    }
}