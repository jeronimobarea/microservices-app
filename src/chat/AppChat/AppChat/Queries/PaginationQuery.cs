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

        public int Page { get; set; }
        public int PerPage { get; set; }     
    }
}