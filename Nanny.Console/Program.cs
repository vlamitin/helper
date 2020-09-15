using Nanny.Console.Visualization;

namespace Nanny.Console
{
    public class Program
    {
        private Output _output;

        public Program()
        {
            _output = new Output();
        }
        
        static void Main(string[] args)
        {
            Program program = new Program();
            program.Run(args);
        }

        public void Run(string[] args)
        {
            _output.Parse(args);
        }
    }
}
