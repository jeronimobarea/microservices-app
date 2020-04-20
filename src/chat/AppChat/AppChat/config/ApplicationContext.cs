using AppChat.models;
using Microsoft.EntityFrameworkCore;

namespace AppChat.config
{
    public class ApplicationContext : DbContext
    {
        public ApplicationContext(DbContextOptions<ApplicationContext> options) : base(options)
        {
        }

        public DbSet<Chat> Chats { get; set; }
    }
}