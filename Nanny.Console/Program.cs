using Nanny.Console.Commands;
using Nanny.Console.Printers;

namespace Nanny.Console
{
    public class Program
    {
        private CommandList _commands;

        public Program()
        {
            _commands = new CommandList();
            _commands.Add(new VersionCommand());
            _commands.Add(new HelpCommand());
        }
        
        static void Main(string[] args)
        {
            Program program = new Program();
            program.Run(args);
        }

        public void Run(string[] args)
        {
            new ConsolePrinter(_commands.Find(args, new HelpCommand())).Print();
        }
    }
}
