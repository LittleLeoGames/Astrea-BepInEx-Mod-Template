using UnityEngine;
using Astrea;
using Astrea.BattleActions;
using Astrea.GameElements;
using System.Reflection;

namespace AstreaBepInExModTemplate.Patches.BattleActions
{
    public class BattleActionExample : BattleAction
    {
        public override void SetupModdedBattleAction()
        {
            SetupModdedBattleAction("BattleActionExample", //Action Name
                "Deal {0} Purification to an enemy. Then reroll its die.", // {0} will be replaced with the value of the die face.
                BattleActionInteractionEnum.PURIFY, //How the action will be affected by effects. 
                                                    //The BattleActionInteractionEnum.PURIFY for instance will be affected by Empower. 
                                                    //If the action won't be affected by any effect, change to BattleActionInteractionEnum.NONE.
                                                    //If the action will be affect by Doom and is mandatory, change to BattleActionInteractionEnum.CORRUPT.
                                                    //If the action is mandatory, but won't be affected by doom, change to BattleActionInteractionEnum.MANDATORY.
                DiceActionLogicsList.DiceActionLogicEnum.DiceActionLogic_ChooseEnemy, //The target of the action, this will change the input of the action.
                ModHelper.Instance.GetModSprite(Assembly.GetExecutingAssembly(), 
                "PurifyEnemyReroll.png")); //Action image name (the same name as the image added to the Resources Folder)
        }

        public override void CastTargetAmount(GameObject target, int amount, GameObject source)
        {
            var purifyEnemyAction = ModHelper.Instance.BattleActionsList.GetBattleAction("PurifyEnemy");
            purifyEnemyAction.CastTargetAmount(target, amount, source);

            var diceInstancesToRoll = target.GetComponent<UnitsDiceActivation>().GetDiceInstancesToRoll();
            if (diceInstancesToRoll.Count > 0)
            {
                var rerollAction = ModHelper.Instance.BattleActionsList.GetBattleAction("Reroll") as RerollAction;
                rerollAction.ExternalCast(diceInstancesToRoll, RollDiceActionType.EXTERNALREROLL, null);
            }
        }
    }
}