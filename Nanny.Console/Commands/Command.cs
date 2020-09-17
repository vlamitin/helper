namespace Nanny.Console.Commands
{
    public abstract class Command
    {
        public abstract void Execute();
        public abstract string Output();
        public abstract Key Key();

        public bool IsSuite(string name)
        {
            return Key().IsSuite(name);
        }
    }
}