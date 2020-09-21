using Microsoft.Extensions.Logging;
using Nanny.Console.Commands;

namespace Nanny.Console.Printers
{
    public class ConsolePrinter : Printer
    {
        private ILogger<ConsolePrinter> _log;
        
        public ConsolePrinter(ILogger<ConsolePrinter> log, Command command) : base(command)
        {
            _log = log;
        }

        public override void Print()
        {
            _log.LogInformation("Start printing");
            WriteLine(Command.Output());
        }

        private void WriteLine(string output)
        {
            System.Console.WriteLine(output);
        }
    }
}