using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.IO;
using UnityEngine;
using ColossalFramework.Math;
using ColossalFramework;
using ColossalFramework.IO;
using ICities;
using ObjUnity3D;
using ModTools;
using System.Reflection;

namespace BuildingsExport
{
    public static class Log
    {
        private static readonly string PREPEND_TAG = Assembly.GetExecutingAssembly().GetName().Name + ": ";
        public static void Message(string s)
        {
            Debug.Log(PREPEND_TAG + s);
        }

        public static void Error(string s)
        {
            Debug.LogError(PREPEND_TAG + s);
        }
        public static void Warning(string s)
        {
            Debug.LogWarning(PREPEND_TAG + s);
        }
    }

    public class BuildingExport: LoadingExtensionBase, IUserMod
    {
        public static GameObject gameObject;

        
        public override void OnLevelLoaded(LoadMode mode)
        {
            base.OnLevelLoaded(mode);
            if (mode != LoadMode.NewGame && mode != LoadMode.LoadGame)
            {
                return;
            }

            if (gameObject != null)
            {
                return;
            }
            gameObject = new GameObject("SpawnVehiclesMod");
            gameObject.AddComponent<BuildingExportLogic>();
        }
        public override void OnLevelUnloading()
        {
            base.OnLevelUnloading();

            if (gameObject == null)
            {
                return;
            }
            UnityEngine.Object.Destroy(gameObject);
            gameObject = null;
        }

        public string Name
        {
            get { return "Export Buildings Custom"; }
        }

        public string Description
        {
            get { return "export buildings position and type at every frame"; }
        }
    }
    public class BuildingExportLogic : MonoBehaviour
    {
        public bool enableExport = false;
        public string FullSessionDirectoryName;

        void Awake()
        {
            if (!Directory.Exists(DataLocation.localApplicationData + @"\ModConfig\"))
                Directory.CreateDirectory(DataLocation.localApplicationData + @"\ModConfig\");
            if (!Directory.Exists(DataLocation.localApplicationData + @"\ModConfig\BuildingExport\"))
                Directory.CreateDirectory(DataLocation.localApplicationData + @"\ModConfig\BuildingExport\");
            if (!Directory.Exists(DataLocation.localApplicationData + @"\ModConfig\BuildingExport\"))
                Directory.CreateDirectory(DataLocation.localApplicationData + @"\ModConfig\BuildingExport\");

            string sessionDirectoryName = "GameSession-" + DateTime.Now.ToString("yyyyMMddHHmmss");
            FullSessionDirectoryName = DataLocation.localApplicationData + @"\ModConfig\BuildingExport\" + sessionDirectoryName + @"\";
            if (!Directory.Exists(FullSessionDirectoryName))
                Directory.CreateDirectory(FullSessionDirectoryName);
            if(!Directory.Exists(FullSessionDirectoryName + @"\meshes\"))
                Directory.CreateDirectory(FullSessionDirectoryName + @"\meshes\");
        }
        void OnGUI()
        {   
            if (enableExport)
            {
                GUI.color = Color.red;
                if (GUI.Button(new Rect(Screen.width - 150, 100, 145, 30), "Building Export : ON"))
                    enableExport = !enableExport;
                GUI.color = Color.white;
            }
            else
            {
                if (GUI.Button(new Rect(Screen.width - 150, 100, 145, 30), "Building Export : OFF"))
                    enableExport = !enableExport;
            }
        }
        void Update()
        {
            if (enableExport)
            {
                Log.Message(FullSessionDirectoryName + "building_pos_angle" + ".txt");
                TextWriter tw = new StreamWriter(FullSessionDirectoryName + "building_pos_angle" + ".txt");
                tw.WriteLine("Camera :");
                tw.WriteLine("position : " + Camera.main.transform.position.ToString());
                var rot = Camera.main.transform.rotation;
                tw.WriteLine("rotation : (" + rot.x + ", " + rot.y + ", " + rot.z + ", " + rot.w + ")");
                Building[] buildings = BuildingManager.instance.m_buildings.m_buffer;
                for (int i = 0; i < buildings.Count(); i++)
                {
                    Building b = buildings[i];
                        
                    if (b.Info.m_lodMesh is null)
                    {
                        Log.Message($"Building {i} has no mesh available!");
                    }
                    else
                    {
                        string objDirectory = FullSessionDirectoryName + "meshes\\" + i.ToString() + ".obj";
                        Log.Message(objDirectory);
                        var objFile = new FileStream(objDirectory, FileMode.Create);
                        tw.WriteLine("BUILDING: " + i.ToString() + " " + b.m_position.ToString() + " " + b.m_angle.ToString() + " " + b.Info.m_size.ToString());
                        OBJLoader.ExportOBJ(b.Info.m_lodMesh.EncodeOBJ(), objFile);
                    }
                }
                tw.Close();
                enableExport = !enableExport;
            }
        }
    }
}
