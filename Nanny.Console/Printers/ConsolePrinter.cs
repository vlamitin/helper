using Nanny.Console.Commands;

namespace Nanny.Console.Printers
{
    public class ConsolePrinter : Printer
    {
        public ConsolePrinter(Command command) : base(command)
        {
            
        }

        public override void Print()
        {
            System.Console.WriteLine(Command.Output());
        }
    }
}