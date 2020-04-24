using System.Collections.Generic;
using System.Text.Json.Serialization;

namespace AppChat.Response
{
    public class PagedResponse<T>
    {
        public PagedResponse()
        {
        }

        public PagedResponse(IEnumerable<T> results)
        {
            Results = results;
        }

        [JsonPropertyName("results")] public IEnumerable<T> Results { get; set; }
        [JsonPropertyName("page")] public int? Page { get; set; }
        [JsonPropertyName("per_page")] public int? PerPage { get; set; }
        [JsonPropertyName("total_pages")] public int? TotalPages { get; set; }
        [JsonPropertyName("has_next")] public bool? HasNext { get; set; }
    }
}