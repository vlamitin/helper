namespace Nanny.Console.Commands
{
    public class VersionCommand : Command
    {
        private string _template =
            "Nanny version: {0}";
        private Key _key = new Key("version", "v");
        
        public override void Execute()
        {
            // nothing
        }

        public override string Output()
        {
            return string.Format(_template, typeof(VersionCommand).Assembly.GetName().Version);
        }

        public override Key Key()
        {
            return _key;
        }
    }
}