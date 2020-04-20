namespace AppChat.Response
{
    public class Response<T>
    {
        public Response(){}

        public Response(T response)
        {
            Results = response;
        }
        
        public T Results { get; set; }
    }
}