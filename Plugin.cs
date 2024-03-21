using BepInEx;
using BepInEx.Logging;
using HarmonyLib;
using System.Reflection;

namespace AstreaBepInExModTemplate
{
    [BepInPlugin(MyPluginInfo.PLUGIN_GUID, MyPluginInfo.PLUGIN_NAME, MyPluginInfo.PLUGIN_VERSION)]
    [BepInProcess("Astrea.exe")]
    public class Plugin : BaseUnityPlugin
    {
        internal static ManualLogSource PluginLogger;

        public Plugin()
        {
            // Keep the default plugin log source around so we don't have to create ManualLogSources everywhere.
            // PluginLogger = Log;
        }

        private void Awake()
        {
            var harmony = new Harmony(MyPluginInfo.PLUGIN_GUID);
            harmony.PatchAll(Assembly.GetExecutingAssembly());
        }
    }
}