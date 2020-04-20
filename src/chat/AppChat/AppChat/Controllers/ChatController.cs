using System;
using System.Collections.Generic;
using System.Linq;
using System.Threading.Tasks;
using AppChat.config;
using AppChat.Domain;
using AppChat.models;
using AppChat.Queries;
using AppChat.Response;
using AutoMapper;
using FireSharp.Config;
using FireSharp.Interfaces;
using Microsoft.AspNetCore.Mvc;

namespace AppChat.Controllers
{
    [Route("[controller]")]
    [ApiController]
    public class ChatController : ControllerBase
    {
        private readonly ApplicationContext _context;
        private readonly IMapper _mapper;

        private readonly IFirebaseConfig _firebaseConfig = new FirebaseConfig
        {
            AuthSecret = "74fpIphhf7mdRApMbs5kkdGJQ1IyaKFcsjCdKNb4",
            BasePath = "https://app-from-idea-to-code.firebaseio.com/"
        };

        private readonly IFirebaseClient _firebaseClient;

        public ChatController(ApplicationContext context, IMapper mapper)
        {
            _context = context;
            _mapper = mapper;
            _firebaseClient = new FireSharp.FirebaseClient(_firebaseConfig);

            Console.WriteLine(_firebaseClient != null
                ? "Firebase connection successful"
                : "Error in firebase connection");
        }

        [HttpGet("active")]
        public OkObjectResult GetActiveUserChats([FromQuery] PaginationQuery paginationQuery, string userId)
        {
            var paginationFilter = _mapper.Map<PaginationFilter>(paginationQuery);
            var totalPages = _context.Chats.Count(c => c.Id != null);
            var chatResponse = _context.Chats
                .Where(c => c.ChatCreator == userId || c.RequestedUser == userId).Where(c => c.Status.Equals("1"))
                .OrderBy(c => c.CreationDate)
                .ToList()
                .Skip(paginationFilter.Page)
                .Take(paginationFilter.PerPage);

            var paginationResponse = new PagedResponse<Chat>(chatResponse)
            {
                Page = paginationFilter.Page,
                PerPage = paginationFilter.PerPage,
                TotalPages = totalPages / paginationFilter.PerPage,
                HasNext = (totalPages / paginationFilter.PerPage) > paginationFilter.Page ? true : false
            };

            return Ok(paginationResponse);
        }

        [HttpGet("pending")]
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

            var paginationResponse = new PagedResponse<Chat>(chatResponse)
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

        [HttpGet("{id}", Name = "GetById")]
        public async Task<OkObjectResult> Get(string id)
        {
            var chat = await _context.FindAsync<Chat>(Guid.Parse(id));

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