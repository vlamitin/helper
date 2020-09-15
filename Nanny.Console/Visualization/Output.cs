namespace Nanny.Console.Visualization
{
    public class Output
    {
        public void Write(string format, params object[] arg)
        {
            System.Console.WriteLine(format, arg);
        }
        
        public void Write(string format)
        {
            System.Console.WriteLine(format);
        }

        public void Parse(string[] args)
        {
            if (args[0] == "--version" || args[0] == "--v")
            {
                Write("Nanny version: {0}", typeof(Output).Assembly.GetName().Version);
            }
            else
            {
                Write("Hello, World!");
            }
        }
    }
}