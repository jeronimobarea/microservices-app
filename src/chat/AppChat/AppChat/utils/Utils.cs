using System;
using System.Collections.Generic;
using System.Linq;
using System.Net.Http;
using System.Text;
using System.Threading.Tasks;
using AppChat.models;
using Newtonsoft.Json;

namespace AppChat.utils
{
    public class Utils
    {
        private static readonly HttpClient client = new HttpClient();

        public async Task<IEnumerable<Chat>> fillChatData(List<Chat> chats)
        {
            var data = new List<string>();
            foreach (var chat in chats)
            {
                data.Add(chat.ChatCreator);
                data.Add(chat.RequestedUser);
            }

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

            var usersList = await response.Content.ReadAsAsync<List<UserData>>().ConfigureAwait(false);
            
            for (var i = 0; i < chats.Count(); i++)
            {
                for (var j = 0; j < usersList.Count(); j++)
                {
                    if (i > j)
                    {
                        j = 0;
                    }

                    if (chats.ToList()[i].ChatCreator == usersList[j].Id)
                    {
                        chats.ToList()[i].CreatorData = usersList[j];
                    }
                    else if (chats.ToList()[i].RequestedUser == usersList[j].Id)
                    {
                        chats.ToList()[i].RequestedUserData = usersList[j];
                    }
                }
            }
            return chats;
        }
    }
}