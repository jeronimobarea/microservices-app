using System.Collections.Generic;

namespace AppChat.Response
{
    public class PagedResponse<T>
    {
        public  PagedResponse(){}

        public PagedResponse(IEnumerable<T> results)
        {
            Results = results;
        }
        
        public IEnumerable<T> Results { get; set; }
        public int? Page { get; set; }
        public int? PerPage { get; set; }
        public int? TotalPages { get; set; }
        public bool? HasNext { get; set; } 
    }
}