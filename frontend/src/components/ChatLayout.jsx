import React, { useState, useEffect, useRef } from 'react';
import { useLocation } from 'react-router-dom';
import Navbar from './Navbar';

// ChatLayout component - A special layout for chat pages with no footer and direct content
export default function ChatLayout({ children }) {
  const location = useLocation();
  const isChatRoute = location.pathname === '/chat';
  const [lastScrollTop, setLastScrollTop] = useState(0);
  const [navbarVisible, setNavbarVisible] = useState(true);
  const scrollThreshold = 15; // minimum scroll distance before hiding navbar
  const scrollTimer = useRef(null);
  const chatContainerRef = useRef(null);
  const scrollDirectionRef = useRef('none'); // Track scroll direction to prevent flickering
  const navbarTransitionTimeout = useRef(null);
  const isScrollingRef = useRef(false); // Track active scrolling
  
  useEffect(() => {
    if (!isChatRoute) {
      // Only apply sliding navbar on chat route
      setNavbarVisible(true);
      return;
    }
    
    // Initial delay to let the DOM settle
    const initialDelay = setTimeout(() => {
      // Get reference to the chat container
      chatContainerRef.current = document.querySelector('.chat-messages-container');
    }, 100);
    
    const handleScroll = (e) => {
      // Mark that scrolling is happening
      isScrollingRef.current = true;
      
      // Use requestAnimationFrame for better performance during scroll
      if (scrollTimer.current) {
        window.cancelAnimationFrame(scrollTimer.current);
      }
      
      scrollTimer.current = window.requestAnimationFrame(() => {
        // Get the element that's being scrolled
        const target = e?.target;
        const isContainerScroll = target && 
          (target.classList?.contains('chat-messages-container') || 
           target.closest('.chat-messages-container'));
        
        // Use the appropriate scroll position
        let st;
        
        if (isContainerScroll) {
          st = target.scrollTop;
        } else if (chatContainerRef.current) {
          st = chatContainerRef.current.scrollTop;
        } else {
          st = window.scrollY || document.documentElement.scrollTop;
        }
        
        // Determine scroll direction with debounce
        if (st > lastScrollTop + scrollThreshold) {
          // Scrolling down - hide navbar with debounce
          if (scrollDirectionRef.current !== 'down') {
            scrollDirectionRef.current = 'down';
            
            // Clear any pending visibility changes
            if (navbarTransitionTimeout.current) {
              clearTimeout(navbarTransitionTimeout.current);
            }
            
            // Apply change after a small delay to prevent flickering
            navbarTransitionTimeout.current = setTimeout(() => {
              setNavbarVisible(false);
            }, 50);
          }
        } else if (st < lastScrollTop - 5) { // Less threshold for showing the navbar
          // Scrolling up - show navbar immediately
          if (scrollDirectionRef.current !== 'up') {
            scrollDirectionRef.current = 'up';
            
            // Clear any pending visibility changes
            if (navbarTransitionTimeout.current) {
              clearTimeout(navbarTransitionTimeout.current);
            }
            
            setNavbarVisible(true);
          }
        } else if (st === 0) {
          // At the top - always show navbar
          setNavbarVisible(true);
        }
        
        // Update last scroll position
        setLastScrollTop(st <= 0 ? 0 : st);
        scrollTimer.current = null;
        
        // Reset scrolling flag after a delay
        setTimeout(() => {
          isScrollingRef.current = false;
        }, 100);
      });
    };
    
    // Use passive event listeners for better performance
    window.addEventListener('scroll', handleScroll, { passive: true });
    
    // Add scroll event to the chat container after it's been found
    const addContainerListener = setInterval(() => {
      if (chatContainerRef.current) {
        chatContainerRef.current.addEventListener('scroll', handleScroll, { passive: true });
        clearInterval(addContainerListener);
      }
    }, 200);
    
    // Force check scroll position periodically to ensure navbar state is correct
    const initTimeout = setTimeout(() => {
      handleScroll();
    }, 500);
    
    return () => {
      window.removeEventListener('scroll', handleScroll);
      
      if (chatContainerRef.current) {
        chatContainerRef.current.removeEventListener('scroll', handleScroll);
      }
      
      if (scrollTimer.current) {
        window.cancelAnimationFrame(scrollTimer.current);
      }
      
      if (navbarTransitionTimeout.current) {
        clearTimeout(navbarTransitionTimeout.current);
      }
      
      clearTimeout(initialDelay);
      clearTimeout(initTimeout);
      clearInterval(addContainerListener);
    };
  }, [lastScrollTop, isChatRoute]);
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-50 via-blue-50 to-indigo-50 flex flex-col w-full overflow-x-hidden">
      <div className={`navbar-wrapper ${isChatRoute ? 'sliding-navbar' : ''} ${navbarVisible || !isChatRoute ? 'navbar-visible' : 'navbar-hidden'}`}>
        <Navbar />
      </div>
      <main className={`flex-1 relative overflow-hidden p-0 w-full ${isChatRoute ? 'chat-main-content' : ''}`}>
        {children}
      </main>
      {/* No Footer component here */}
    </div>
  );
}
