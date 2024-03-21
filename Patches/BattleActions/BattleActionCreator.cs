using UnityEngine;
using Astrea;
using HarmonyLib;

namespace AstreaBepInExModTemplate.Patches.BattleActions
{
    public class BattleActionCreator
    {
        [HarmonyPatch(typeof(ModHelper), nameof(ModHelper.Initialize))]
        public class ModHelper_Initialize
        {
            public static void Prefix(ModHelper __instance)
            {
                Debug.Log("*******PREFIX MODHELPER_INITIALIZE");
                if (__instance == null)
                {
                    Debug.Log("*******ERROR_PLUGIN 0");
                    return;
                }
                
                __instance.CreateBattleAction(new BattleActionExample());
            }
        }
    }
}
