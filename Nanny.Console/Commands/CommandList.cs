using System.Collections.Generic;

namespace Nanny.Console.Commands
{
    public class CommandList : List<Command>
    {
        public CommandList()
        {
            Add(new VersionCommand());
            Add(new HelpCommand());
        }

        public Command Find(string[] userInput, Command defaultValue)
        {
            if (userInput.Length == 0)
            {
                return defaultValue;
            }

            Command candidate = Find(command => command.IsSuite(userInput[0]));

            return candidate == null ? defaultValue : candidate;
        }
    }
}