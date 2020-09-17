using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;

namespace Nanny.Console.Commands
{
    public class CommandList : List<Command>
    {
        private Regex _regex = new Regex("(--[a-z]*)");
        public Command Find(string[] userInput, Command defaultValue)
        {
            if (userInput.Length == 0)
            {
                return defaultValue;
            }

            Command candidate = Find(command => command.IsSuite(userInput[0]));

            if (candidate == null)
            {
                return defaultValue;
            }
            else
            {
                return candidate;
            }
        }
    }
}