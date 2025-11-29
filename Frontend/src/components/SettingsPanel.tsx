import React, { useState, useEffect } from "react";
import { supabase } from "../lib/supabase";
import { Session } from "@supabase/supabase-js";
import { LoginPage } from "./LoginPage";

export interface SettingsPanelProps {
  isVisible: boolean;
  onClose: () => void;
}

export const SettingsPanel: React.FC<SettingsPanelProps> = ({
  isVisible,
  onClose,
}) => {
  const [session, setSession] = useState<Session | null>(null);
  const [loading, setLoading] = useState(true);
  const [showLoginPage, setShowLoginPage] = useState(false);

  useEffect(() => {
    supabase.auth.getSession().then(({ data: { session } }) => {
      setSession(session);
      setLoading(false);
    });

    const {
      data: { subscription },
    } = supabase.auth.onAuthStateChange((_event, session) => {
      setSession(session);
      if (session) {
        setShowLoginPage(false);
      }
    });

    return () => subscription.unsubscribe();
  }, []);

  const handleSignOut = async () => {
    await supabase.auth.signOut();
  };

  const handleLoginSuccess = () => {
    setShowLoginPage(false);
  };

  return (
    <>
      <div
        className={`fixed 
          bottom-4 left-4 right-4
          sm:left-22 sm:right-4
          top-20 sm:top-4
          frosted-glass 
          transform transition-all duration-300 ease-in-out z-40 
          overflow-hidden
          flex flex-col
          ${
            isVisible
              ? "translate-y-0 opacity-100"
              : "translate-y-full opacity-0 pointer-events-none"
          }
        `}
      >
        {/* Header */}
        <div className="flex items-center justify-between p-4 border-b border-stone/20">
          <div className="flex items-center gap-3">
            <svg
              className="w-5 h-5 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"
              />
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
              />
            </svg>
            <h3 className="text-base font-medium text-white">Settings</h3>
          </div>
          <button
            onClick={onClose}
            className="p-1 hover:bg-bangladesh-green rounded-full transition-colors"
          >
            <svg
              className="w-4 h-4 text-gray-400"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth="2"
                d="M6 18L18 6M6 6l12 12"
              />
            </svg>
          </button>
        </div>

        <div className="w-full h-px bg-stone mb-4"></div>

        {/* Content */}
        <div className="flex-1 overflow-y-auto dark-scrollbar p-4">
          {loading ? (
            <div className="flex items-center justify-center h-full">
              <div className="animate-spin h-6 w-6 border-2 border-caribbean-green border-t-transparent rounded-full"></div>
            </div>
          ) : !session ? (
            <div className="flex flex-col items-center justify-center h-full text-center max-w-md mx-auto py-8">
              <div className="w-16 h-16 bg-bangladesh-green/20 flex items-center justify-center mb-4">
                <svg
                  className="w-8 h-8 text-bangladesh-green"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth="2"
                    d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z"
                  />
                </svg>
              </div>
              <h3 className="text-xl font-bold text-white mb-2">
                Uh oh, it seems you are not signed in yet.
              </h3>
              <p className="text-stone text-sm mb-6">
                You can make an account here and get notifications, it's free!
              </p>

              <button
                onClick={() => setShowLoginPage(true)}
                className="px-6 py-2.5 bg-bangladesh-green hover:bg-mountain-meadow rounded-lg text-white hover:text-dark-green font-semibold transition-colors"
              >
                Sign In / Sign Up
              </button>
            </div>
          ) : (
            <div className="max-w-2xl mx-auto space-y-4">
              {/* Account Info */}
              <div className="flex items-center gap-3 p-3 bg-white/5">
                <div className="w-10 h-10 bg-bangladesh-green flex items-center justify-center text-white font-bold text-lg">
                  {session.user.email?.[0].toUpperCase()}
                </div>
                <div className="flex-1 min-w-0">
                  <h4 className="text-white font-medium text-sm truncate">
                    {session.user.email}
                  </h4>
                  <p className="text-stone text-xs">Account Active</p>
                </div>
                <button
                  onClick={handleSignOut}
                  className="text-xs text-red-400 hover:text-red-300 font-medium px-2 py-1"
                >
                  Sign Out
                </button>
              </div>

              {/* Notifications Section */}
              <div className="bg-white/5 p-4">
                <div className="flex items-center gap-2 mb-3">
                  <svg
                    className="w-4 h-4 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9"
                    />
                  </svg>
                  <span className="text-sm text-gray-400 font-medium">
                    Notifications
                  </span>
                </div>
                <div className="space-y-3">
                  <label className="flex items-center justify-between cursor-pointer hover:bg-rich-black/30 p-2 rounded">
                    <span className="text-sm text-gray-300">Email Alerts</span>
                    <input
                      type="checkbox"
                      className="filter-checkbox"
                      defaultChecked
                    />
                  </label>
                  <label className="flex items-center justify-between cursor-pointer hover:bg-rich-black/30 p-2 rounded">
                    <span className="text-sm text-gray-300">
                      Push Notifications
                    </span>
                    <input
                      type="checkbox"
                      className="filter-checkbox"
                      defaultChecked
                    />
                  </label>
                  <label className="flex items-center justify-between cursor-pointer hover:bg-rich-black/30 p-2 rounded">
                    <span className="text-sm text-gray-300">Weekly Digest</span>
                    <input type="checkbox" className="filter-checkbox" />
                  </label>
                </div>
              </div>

              {/* Preferences Section */}
              <div className="bg-white/5 p-4">
                <div className="flex items-center gap-2 mb-3">
                  <svg
                    className="w-4 h-4 text-gray-400"
                    fill="none"
                    stroke="currentColor"
                    viewBox="0 0 24 24"
                  >
                    <path
                      strokeLinecap="round"
                      strokeLinejoin="round"
                      strokeWidth="2"
                      d="M12 6V4m0 2a2 2 0 100 4m0-4a2 2 0 110 4m-6 8a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4m6 6v10m6-2a2 2 0 100-4m0 4a2 2 0 110-4m0 4v2m0-6V4"
                    />
                  </svg>
                  <span className="text-sm text-gray-400 font-medium">
                    Preferences
                  </span>
                </div>
                <div className="space-y-3">
                  <label className="flex items-center justify-between cursor-pointer hover:bg-rich-black/30 p-2 rounded">
                    <span className="text-sm text-gray-300">Dark Mode</span>
                    <input
                      type="checkbox"
                      className="filter-checkbox"
                      defaultChecked
                      disabled
                    />
                  </label>
                  <label className="flex items-center justify-between cursor-pointer hover:bg-rich-black/30 p-2 rounded">
                    <span className="text-sm text-gray-300">
                      Location Services
                    </span>
                    <input
                      type="checkbox"
                      className="filter-checkbox"
                      defaultChecked
                    />
                  </label>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>

      {/* Login Page Modal */}
      <LoginPage
        isVisible={showLoginPage}
        onClose={() => setShowLoginPage(false)}
        onSuccess={handleLoginSuccess}
      />
    </>
  );
};
