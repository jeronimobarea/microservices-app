using System.Text.Json.Serialization;

namespace AppChat.Queries
{
    public class PaginationQuery
    {
        public PaginationQuery()
        {
            Page = 0;
            PerPage = 10;
        }

        public PaginationQuery(int page, int perPage)
        {
            Page = page;
            PerPage = perPage;
        }

        [JsonPropertyName("page")] public int Page { get; set; }
        [JsonPropertyName("per_page")] public int PerPage { get; set; }
    }
}