import React, { useState, Fragment } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { Disclosure, Menu, Transition } from '@headlessui/react';
import { 
  Bars3Icon, 
  XMarkIcon, 
  ShoppingCartIcon, 
  ChatBubbleLeftRightIcon,
  HomeIcon,
  CubeIcon,
  ClipboardDocumentListIcon,
  UserCircleIcon,
  Cog6ToothIcon,
  ArrowRightOnRectangleIcon,
  SparklesIcon,
  BellIcon
} from '@heroicons/react/24/outline';
import { useAuth } from '../contexts/AuthContext';

function classNames(...classes) {
  return classes.filter(Boolean).join(' ');
}

export default function Navbar() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();
  const [cartCount] = useState(0); // This would come from cart context in real app

  const navigation = [
    { name: 'Home', href: '/', icon: HomeIcon, current: location.pathname === '/' },
    { name: 'AI Assistant', href: '/chat', icon: ChatBubbleLeftRightIcon, current: location.pathname === '/chat' },
    { name: 'Products', href: '/products', icon: CubeIcon, current: location.pathname === '/products' },
    { name: 'Orders', href: '/orders', icon: ClipboardDocumentListIcon, current: location.pathname === '/orders' },
  ];

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };  return (
    <Disclosure as="nav" className="bg-white shadow-lg border-b border-gray-200 sticky top-0 z-50 w-full">
      {({ open }) => (
        <>
          <div className="w-full mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              {/* Logo and Brand */}
              <div className="flex items-center">
                <Link to="/" className="flex items-center space-x-3">
                  <div className="bg-gradient-to-r from-blue-600 to-purple-600 rounded-xl p-2 shadow-lg">
                    <SparklesIcon className="w-6 h-6 text-white" />
                  </div>
                  <div className="hidden sm:block">
                    <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                      NexTechAI
                    </h1>
                    <p className="text-xs text-gray-500 -mt-1">Smart Shopping Assistant</p>
                  </div>
                </Link>
              </div>

              {/* Desktop Navigation */}
              <div className="hidden md:flex items-center space-x-1">
                {navigation.map((item) => (
                  <Link
                    key={item.name}
                    to={item.href}
                    className={classNames(
                      item.current
                        ? 'bg-blue-50 text-blue-700 border-blue-200'
                        : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50 border-transparent',
                      'inline-flex items-center px-4 py-2 border-b-2 text-sm font-medium transition-all duration-200 rounded-lg mx-1'
                    )}
                  >
                    <item.icon className="w-4 h-4 mr-2" />
                    {item.name}
                  </Link>
                ))}
              </div>

              {/* Right Side Actions */}
              <div className="flex items-center space-x-4">
                {/* Notifications */}
                <button className="relative p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200">
                  <BellIcon className="w-5 h-5" />
                  <span className="absolute top-1 right-1 block h-2 w-2 rounded-full bg-red-400"></span>
                </button>

                {/* Cart */}
                <Link
                  to="/cart"
                  className="relative p-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 rounded-lg transition-colors duration-200"
                >
                  <ShoppingCartIcon className="w-5 h-5" />
                  {cartCount > 0 && (
                    <span className="absolute -top-1 -right-1 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center font-medium">
                      {cartCount}
                    </span>
                  )}
                </Link>

                {/* User Menu */}
                <Menu as="div" className="relative">
                  <div>
                    <Menu.Button className="flex items-center space-x-3 text-sm rounded-lg p-2 hover:bg-gray-50 transition-colors duration-200">
                      <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                        <span className="text-white font-semibold text-sm">
                          {user?.username ? user.username[0].toUpperCase() : 'U'}
                        </span>
                      </div>
                      <div className="hidden md:block text-left">
                        <p className="text-sm font-medium text-gray-900">
                          {user?.username || 'User'}
                        </p>
                        <p className="text-xs text-gray-500">Premium Member</p>
                      </div>
                    </Menu.Button>
                  </div>
                  <Transition
                    as={Fragment}
                    enter="transition ease-out duration-100"
                    enterFrom="transform opacity-0 scale-95"
                    enterTo="transform opacity-100 scale-100"
                    leave="transition ease-in duration-75"
                    leaveFrom="transform opacity-100 scale-100"
                    leaveTo="transform opacity-0 scale-95"
                  >
                    <Menu.Items className="absolute right-0 z-10 mt-2 w-56 origin-top-right rounded-xl bg-white shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none border border-gray-200">
                      <div className="p-2">
                        <div className="px-3 py-2 border-b border-gray-100 mb-2">
                          <p className="text-sm font-medium text-gray-900">{user?.username}</p>
                          <p className="text-xs text-gray-500">{user?.email}</p>
                        </div>
                        
                        <Menu.Item>
                          {({ active }) => (
                            <Link
                              to="/profile"
                              className={classNames(
                                active ? 'bg-gray-50' : '',
                                'flex items-center px-3 py-2 text-sm text-gray-700 rounded-lg'
                              )}
                            >
                              <UserCircleIcon className="w-4 h-4 mr-3 text-gray-400" />
                              Your Profile
                            </Link>
                          )}
                        </Menu.Item>
                        
                        <Menu.Item>
                          {({ active }) => (
                            <Link
                              to="/settings"
                              className={classNames(
                                active ? 'bg-gray-50' : '',
                                'flex items-center px-3 py-2 text-sm text-gray-700 rounded-lg'
                              )}
                            >
                              <Cog6ToothIcon className="w-4 h-4 mr-3 text-gray-400" />
                              Settings
                            </Link>
                          )}
                        </Menu.Item>
                        
                        <div className="border-t border-gray-100 my-2"></div>
                        
                        <Menu.Item>
                          {({ active }) => (
                            <button
                              onClick={handleLogout}
                              className={classNames(
                                active ? 'bg-red-50 text-red-700' : 'text-gray-700',
                                'flex items-center w-full px-3 py-2 text-sm rounded-lg'
                              )}
                            >
                              <ArrowRightOnRectangleIcon className="w-4 h-4 mr-3 text-gray-400" />
                              Sign out
                            </button>
                          )}
                        </Menu.Item>
                      </div>
                    </Menu.Items>
                  </Transition>
                </Menu>

                {/* Mobile menu button */}
                <div className="md:hidden">
                  <Disclosure.Button className="inline-flex items-center justify-center p-2 rounded-lg text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition-colors duration-200">
                    <span className="sr-only">Open main menu</span>
                    {open ? (
                      <XMarkIcon className="block h-6 w-6" aria-hidden="true" />
                    ) : (
                      <Bars3Icon className="block h-6 w-6" aria-hidden="true" />
                    )}
                  </Disclosure.Button>
                </div>
              </div>
            </div>
          </div>

          {/* Mobile menu */}
          <Disclosure.Panel className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 bg-gray-50 border-t border-gray-200">
              {navigation.map((item) => (
                <Link
                  key={item.name}
                  to={item.href}
                  className={classNames(
                    item.current
                      ? 'bg-blue-100 text-blue-700'
                      : 'text-gray-600 hover:bg-blue-50 hover:text-blue-600',
                    'flex items-center px-3 py-2 rounded-lg text-base font-medium transition-colors duration-200'
                  )}
                >
                  <item.icon className="w-5 h-5 mr-3" />
                  {item.name}
                </Link>
              ))}
              
              <div className="border-t border-gray-300 pt-3 mt-3">
                <div className="flex items-center px-3 py-2">
                  <div className="w-10 h-10 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center mr-3">
                    <span className="text-white font-semibold">
                      {user?.username ? user.username[0].toUpperCase() : 'U'}
                    </span>
                  </div>
                  <div>
                    <p className="text-base font-medium text-gray-900">{user?.username}</p>
                    <p className="text-sm text-gray-500">{user?.email}</p>
                  </div>
                </div>
                
                <Link
                  to="/profile"
                  className="flex items-center px-3 py-2 text-base font-medium text-gray-600 hover:bg-blue-50 hover:text-blue-600 rounded-lg transition-colors duration-200"
                >
                  <UserCircleIcon className="w-5 h-5 mr-3" />
                  Your Profile
                </Link>
                
                <button
                  onClick={handleLogout}
                  className="flex items-center w-full px-3 py-2 text-base font-medium text-gray-600 hover:bg-red-50 hover:text-red-600 rounded-lg transition-colors duration-200"
                >
                  <ArrowRightOnRectangleIcon className="w-5 h-5 mr-3" />
                  Sign out
                </button>
              </div>
            </div>
          </Disclosure.Panel>
        </>
      )}
    </Disclosure>
  );
}
