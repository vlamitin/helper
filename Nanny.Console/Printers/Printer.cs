using Nanny.Console.Commands;

namespace Nanny.Console.Printers
{
    public abstract class Printer
    {
        protected Command Command;
        
        public Printer(Command command)
        {
            Command = command;
        }

        public abstract void Print();
    }
}