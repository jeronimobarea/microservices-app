using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using AppChat.config;
using AppChat.Domain;
using AppChat.models;
using AppChat.Queries;
using AppChat.Response;
using AppChat.utils;
using AutoMapper;
using FireSharp.Config;
using FireSharp.Interfaces;
using Microsoft.AspNetCore.Mvc;
using Newtonsoft.Json;


namespace AppChat.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ChatController : ControllerBase
    {
        private readonly ApplicationContext _context;
        private readonly IMapper _mapper;
        private readonly IFirebaseClient _firebaseClient;
        private readonly Utils _utils = new Utils();
        private static readonly HttpClient client = new HttpClient();

        private readonly IFirebaseConfig _firebaseConfig = new FirebaseConfig
        {
            AuthSecret = "74fpIphhf7mdRApMbs5kkdGJQ1IyaKFcsjCdKNb4",
            BasePath = "https://app-from-idea-to-code.firebaseio.com/"
        };

        public ChatController(ApplicationContext context, IMapper mapper)
        {
            _context = context;
            _mapper = mapper;
            _firebaseClient = new FireSharp.FirebaseClient(_firebaseConfig);

            Console.WriteLine(_firebaseClient != null
                ? "Firebase connection successful"
                : "Error in firebase connection");
        }

        [HttpGet("user/active")]
        public OkObjectResult GetActiveUserChats([FromQuery] PaginationQuery paginationQuery, string userId)
        {
            var paginationFilter = _mapper.Map<PaginationFilter>(paginationQuery);
            var totalPages = _context.Chats.Count(c => c.Id != null);
            var chatResponse = _context.Chats
                .Where(c => c.ChatCreator == userId || c.RequestedUser == userId)
                .Where(c => c.Status.Equals("1"))
                .OrderBy(c => c.CreationDate)
                .ToList()
                .Skip(paginationFilter.Page)
                .Take(paginationFilter.PerPage);

            var filledChat = _utils.fillChatData(chatResponse.ToList());

            var paginationResponse = new PagedResponse<Chat>(filledChat.Result.ToList())
            {
                Page = paginationFilter.Page,
                PerPage = paginationFilter.PerPage,
                TotalPages = totalPages / paginationFilter.PerPage,
                HasNext = (totalPages / paginationFilter.PerPage) > paginationFilter.Page ? true : false
            };

            return Ok(paginationResponse);
        }

        [HttpGet("user/pending")]
        public OkObjectResult GetPendingUserChats([FromQuery] PaginationQuery paginationQuery, string userId)
        {
            var paginationFilter = _mapper.Map<PaginationFilter>(paginationQuery);
            var totalPages = _context.Chats.Count(c => c.Id != null);
            var chatResponse = _context.Chats
                .Where(c => c.ChatCreator == userId || c.RequestedUser == userId).Where(c => c.Status.Equals("0"))
                .OrderBy(c => c.CreationDate)
                .ToList()
                .Skip(paginationFilter.Page)
                .Take(paginationFilter.PerPage);

            var filledChat = _utils.fillChatData(chatResponse.ToList());

            var paginationResponse = new PagedResponse<Chat>(filledChat.Result.ToList())
            {
                Page = paginationFilter.Page,
                PerPage = paginationFilter.PerPage,
                TotalPages = totalPages / paginationFilter.PerPage,
                HasNext = (totalPages / paginationFilter.PerPage) > paginationFilter.Page ? true : false
            };

            return Ok(paginationResponse);
        }

        [HttpGet("active")]
        public IEnumerable<Chat> GetActiveChats()
        {
            return _context.Chats.Where(c => c.IsBlocked == false);
        }

        [HttpGet("blocked")]
        public IEnumerable<Chat> GetBlockedChats()
        {
            return _context.Chats.Where(c => c.IsBlocked);
        }

        [HttpGet("/{id}")]
        public async Task<OkObjectResult> Get([FromQuery] string id)
        {
            var chat = await _context.FindAsync<Chat>(Guid.Parse(id));

            var data = new List<string> {chat.ChatCreator, chat.RequestedUser};

            var url = "http://localhost:8100/profiles/basic/list/";
            var output = JsonConvert.SerializeObject(data.ToArray());

            var request = new HttpRequestMessage
            {
                Method = HttpMethod.Get,
                RequestUri = new Uri(url),
                Content = new StringContent(output, Encoding.UTF8, "application/json"),
            };

            var response = await client.SendAsync(request).ConfigureAwait(false);
            response.EnsureSuccessStatusCode();

            var userList =
                await response.Content.ReadAsAsync<List<UserData>>().ConfigureAwait(false);

            if (chat.ChatCreator == userList[0].Id)
            {
                chat.CreatorData = userList[0];
                chat.RequestedUserData = userList[1];
            }
            else
            {
                chat.CreatorData = userList[1];
                chat.RequestedUserData = userList[0];
            }

            return Ok(chat);
        }

        [HttpPost]
        public async Task<OkObjectResult> Post([FromBody] Chat chat)
        {
            chat.CreationDate = DateTime.UtcNow;
            chat.LastModification = DateTime.UtcNow;
            chat.Status = "0";

            await _context.AddAsync(chat);

            await _context.SaveChangesAsync();

            //var response = await _firebaseClient.SetTaskAsync("chat/" + chat.Id, chat);
            //var result = response.ResultAs<Chat>();

            //Console.WriteLine("Firebase chat inserted " + result.Id);

            return Ok(chat);
        }

        [HttpPatch("accept")]
        public async Task<OkObjectResult> AcceptChat(string id)
        {
            var chat = await _context.FindAsync<Chat>(Guid.Parse(id));

            chat.Status = "1";

            await _context.SaveChangesAsync();

            return Ok("Chat accepted");
        }

        [HttpPatch("decline")]
        public async Task<OkObjectResult> DeclineChat(string id)
        {
            var chat = await _context.FindAsync<Chat>(Guid.Parse(id));

            //_context.Chats.Remove(chat);
            chat.Status = "2";

            await _context.SaveChangesAsync();

            return Ok("Chat declined");
        }
    }
}