using System;
using System.Threading.Tasks;
using AppChat.config;
using AppChat.models;
using AutoMapper;
using FirebaseAdmin.Messaging;
using FireSharp.Config;
using FireSharp.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AppChat.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class MessageController : Controller
    {
        private readonly ApplicationContext _context;
        private readonly IMapper _mapper;

        private readonly IFirebaseConfig _firebaseConfig = new FirebaseConfig
        {
            AuthSecret = "74fpIphhf7mdRApMbs5kkdGJQ1IyaKFcsjCdKNb4",
            BasePath = "https://app-from-idea-to-code.firebaseio.com/"
        };

        private readonly IFirebaseClient _firebaseClient;

        public MessageController(ApplicationContext context, IMapper mapper)
        {
            _context = context;
            _mapper = mapper;
            _firebaseClient = new FireSharp.FirebaseClient(_firebaseConfig);

            Console.WriteLine(_firebaseClient != null
                ? "Firebase connection successful"
                : "Error in firebase connection");
        }


        [HttpPost]
        public async Task<OkObjectResult> PostMessage([FromBody] ChatMessage message)
        {
            message.Id = Guid.NewGuid();
            message.CreationDate = DateTime.UtcNow;

            var response =
                await _firebaseClient.SetTaskAsync("chats/" + message.ChatId + "/" + message.Id, message);
            var result = response.ResultAs<ChatMessage>();

            Console.WriteLine("Firebase message inserted " + result.Id);

            return Ok(message);
        }
    }
}